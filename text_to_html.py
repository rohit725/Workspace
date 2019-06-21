html = """<!DOCTYPE html>

<html>
<head>
    <title>Conversion</title>
    <style type='text/css'>
        .container-bsemail {
            position: relative;
            border-radius: 10px;
            left: 0;
            right: 0;
            top: 0;
            bottom: 0;
        }
        .table-css{
            background-color: #1e88e5;
            border: 0;
            border-radius: 5px;
            cellspacing: 2;
        }
        .table-row{
            background-color: #FFF;
        }
        .table-header{
            color: #FFF;
        }
    </style>
</head>

<body>
    <div class='container-bsemail'>
        <table class='table-css' cellpadding=7>
%s
        </table>
    </div>
</body>
</html>
"""
#<tr class='table-header'>  <th>Key</th> <th>Value</th> </tr>


def text_to_html(filepath):
    strat_row = "            <tr class='table-row'>"
    end_row = "</tr>"
    rows_list = []
    with open(filepath, 'r') as f:
        lst = f.readlines()
    for count, line in enumerate(lst):
        if count not in [0, len(lst) - 2] and line != '\n':
            lst_values = line.split(':')
            if len(lst_values) == 2:
                lst_values = list(map(str.strip, lst_values))
                rows_list.append(
                    strat_row + "<td>" + lst_values[0] + "</td><td>" + lst_values[1] + "</td>" + end_row)
    final = html % ('\n'.join(rows_list))
    with open('Files/avransom.html', 'w') as f:
        f.write(final)


text_to_html('Files/avransom.txt')
