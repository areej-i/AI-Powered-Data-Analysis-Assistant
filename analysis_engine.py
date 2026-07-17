import pandas as pd


class AnalysisEngine:

    def __init__(self, dataframe):
        self.df = dataframe

    def execute(self, request):
        allowed_operations = {
            "mean",
            "sum",
            "max",
            "min",
            "median",
            "count",
            "missing_values",
            "unique_values"
        }

        operation = request.operation.value.lower()
        
        operation_aliases = {
            "avg": "mean",
            "average": "mean",
            "AVG": "mean",
            "maximum": "max",
            "highest": "max",
            "minimum": "min",
            "lowest": "min"
        }

        operation = operation_aliases.get(
            operation,
            operation
        )

        column = request.value_column
        group_by = request.group_by
        value_column = request.value_column
        
        # Handle missing value analysis
        if operation == "missing_values":
            return {
                "result": self.df.isnull().sum().to_dict()
            }

        if operation == "unique_values":

            return {
                "result": self.df[column].unique().tolist()
            }

        if column and column not in self.df.columns:
            return {"error": f"Column '{column}' does not exist"}
        
        if group_by and group_by not in self.df.columns:
            return {"error": f"Column '{group_by}' does not exist"}
        
        if operation not in allowed_operations:
            return {
                "error": f"I don't know how to perform '{request.operation}' yet."
            }
        
        
        if operation == "count" and not column and not group_by:

            return {
                "result": len(self.df)
            }

        # Handle grouped calculations
        if group_by and value_column:

            if operation == "mean":

                result = (
                    self.df
                    .groupby(group_by)[value_column]
                    .mean()
                    .to_dict()
                )

            elif operation == "sum":

                result = (
                    self.df
                    .groupby(group_by)[value_column]
                    .sum()
                    .to_dict()
                )

            elif operation == "max":

                result = (
                    self.df
                    .groupby(group_by)[value_column]
                    .max()
                    .to_dict()
                )

            elif operation == "min":

                result = (
                    self.df
                    .groupby(group_by)[value_column]
                    .min()
                    .to_dict()
                )

            elif operation == "median":

                result = (
                    self.df
                    .groupby(group_by)[value_column]
                    .median()
                    .to_dict()
                )

            elif operation == "count":

                result = (
                    self.df
                    .groupby(group_by)[value_column]
                    .count()
                    .to_dict()
                )

            else:
                return {
                    "error": f"Unsupported grouped operation: {operation}"
                }


            return {
                "result": result
            }


        # Handle normal column calculations
        if column:

            if operation == "mean":

                return {
                    "result": self.df[column].mean()
                }

            elif operation == "sum":

                return {
                    "result": self.df[column].sum()
                }

            elif operation == "max":

                return {
                    "result": self.df[column].max()
                }

            elif operation == "min":

                return {
                    "result": self.df[column].min()
                }

            elif operation == "median":

                return {
                    "result": self.df[column].median()
                }

            elif operation == "count":

                return {
                    "result": self.df[column].count()
                }

        return {
            "error": f"Unsupported operation: {operation}"
        }