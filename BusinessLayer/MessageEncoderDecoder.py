class MessageEncoderDecoder:
    def __init__(self):
        self.bytes = []

    def push_byte(self, next_byte):
        self.bytes.append(next_byte)

    def decode_next_byte(self, next_byte):
        if next_byte == '\n':
            return self.pop_string()

        self.push_byte(next_byte)
        return None

    def encode(self, message):
        return message.encode('utf-8')

    def pop_string(self):
        return self.bytes.decode("utf-8", "ignore")
