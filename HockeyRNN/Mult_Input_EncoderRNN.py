import torch.nn as nn

class EncoderRNN(nn.Module):

    def __init__(self, vocab_size, age_size, position_size, max_len, 
            hidden_size, input_dropout_p=0, dropout_p=0, n_layers=1, 
            bidirectional=False, rnn_cell='gru', variable_lengths=False):
        super(EncoderRNN, self).__init__(vocab_size, age_size, position_size, 
        max_len, hidden_size, input_dropout_p, dropout_p, n_layers, rnn_cell)

        self.vocab_size = vocab_size
        self.max_len = max_len
        self.hidden_size = hidden_size
        self.n_layers = n_layers
        self.input_dropout_p = input_dropout_p
        self.input_dropout = nn.Dropout(p=input_dropout_p)
        if rnn_cell.lower() == 'lstm':
            self.rnn_cell = nn.LSTM
        elif rnn_cell.lower() == 'gru':
            self.rnn_cell = nn.GRU
        else:
            raise ValueError("Unsupported RNN Cell: {0}".format(rnn_cell))

        self.dropout_p = dropout_p

        self.variable_lengths = variable_lengths
        self.embedding = nn.Embedding(vocab_size, hidden_size)
        self.age_embedding = nn.Embedding(age_size, hidden_size)
        self.position_embedding = nn.Embedding(age_size, hidden_size)
        self.rnn = self.rnn_cell(hidden_size * 3, hidden_size, n_layers,
                                 batch_first=True, bidirectional=bidirectional, dropout=dropout_p)

    def forward(self, input_var, input_ages, input_position, input_lengths=None):
       
        input_embedded = self.embedding(input_var)
        age_embedded = self.age_embedding(input_ages)
        position_embedded = self.position_embedding(input_position)
        embedded = torch.cat((input_embedded, age_embedded, position_embedded), 2)
        embedded = self.input_dropout(embedded)
        if self.variable_lengths:
            embedded = nn.utils.rnn.pack_padded_sequence(embedded, input_lengths, batch_first=True)
        output, hidden = self.rnn(embedded)
        if self.variable_lengths:
            output, _ = nn.utils.rnn.pad_packed_sequence(output, batch_first=True)
        return output, hidden

