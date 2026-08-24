from data_series import DataSeries

class DataFeed:
    def __init__(self, data):
        self.current_index = -1

        self.data = data
        for column in data.columns:
            setattr(self, column, DataSeries(data[column], self))
    
    def add_series(self, series):
        if hasattr(self, series.name):
            raise ValueError(
                f"Cannot add series '{series.name}': "
                "an attribute with this name already exists."
            )
        setattr(self, series.name, DataSeries(series, self))

    def is_finished(self):
        return self.current_index >= len(self.data)

    def next(self):
        if self.is_finished():
            raise StopIteration("No more data available.")
        self.current_index += 1