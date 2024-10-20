# Start creating the HTML report
html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Report</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
        }
        th {
            background-color: #f2f2f2;
        }
        .image-column {
            width: 70%;
        }
        .name-column {
            width: 30%;
        }
    </style>
</head>
<body>
    <h1>URL's Website Views Report</h1>
    <table>
        <tr>
            <th class="image-column">Image</th>
            <th class="name-column">URL Path</th>
        </tr>
'''

def initiate_html_report():
    return html_content

def generate_html_report(html_report, image_data_list, report_path):
    # Populate the table with image data
    for image_data in image_data_list:
        img_path = image_data[0]
        url_path = image_data[1]
        html_report += f'''
            <tr>
                <td class="image-column"><img src="{img_path}" alt="{img_path}" style="max-width: 100%; height: auto;"></td>
                <td class="name-column">{url_path}</td>
            </tr>
        '''
    # Write the HTML content to a file
    with open(f'{report_path}/report.html', 'w') as report_file:
        report_file.write(html_report)
    print(f"HTML report generated successfully in {report_path}/report.html!")
