class DataSeries:
    def __init__(self, values, feed):
        self.values = values
        self.feed = feed

    def __getitem__(self, index):
        """
        data[0] returns present data
        data[-1], ..., returns previous data
        """
        actual_index = self.feed.current_index + index
        if actual_index >= len(self.values) or index > 0:
            raise IndexError("Attempt to access future data.")
        if actual_index < 0:
            raise IndexError("Attempt to access data outside the available range.")
        return self.values.iloc[actual_index]
    