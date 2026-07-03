import pandas as pd
from io import BytesIO


def convert_to_excel(data):

    df = pd.DataFrame(data)

    output = BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='TestCases')

    output.seek(0)

    return output