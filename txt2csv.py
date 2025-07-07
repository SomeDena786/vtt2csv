import os
import csv

def vtt_to_csv(folder_path, output_csv):
    all_rows = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.ja.vtt'):
            base_name = filename[:-7]
            id_start = base_name.find('[')
            id_end = base_name.find(']')
            id_name = ''
            if id_start != -1 and id_end != -1 and id_end > id_start:
                id_name = base_name[id_start+1:id_end]
                base_name = base_name[:id_start] + base_name[id_end+1:]

            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
                lines = f.readlines()

            i = 0
            prev_subtitle = None
            while i < len(lines):
                line = lines[i].strip()
                if '-->' in line:
                    start_time_str = line.split('-->')[0].strip()
                    h, m, s = start_time_str.split(':')
                    s = s.split('.')[0]
                    try:
                        start_seconds = int(h) * 3600 + int(m) * 60 + int(s)
                    except ValueError:
                        i += 1
                        continue
                    subtitle = lines[i + 1].strip() if i + 1 < len(lines) else ''
                    if subtitle != prev_subtitle:
                        # 5列目のURLを生成
                        url = f'https://youtube.com/watch?v={id_name}&t={start_seconds}'
                        all_rows.append([base_name, start_seconds, subtitle, id_name, url])
                        prev_subtitle = subtitle
                    i += 2
                else:
                    i += 1

    with open(output_csv, 'w', newline='', encoding='cp932', errors='replace') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['filename', 'timestamp', 'subtitle', 'id', 'url'])
        writer.writerows(all_rows)

# 使い方例: vtt_to_csv('/Users/someden/Downloads/yt-dlp', '/Users/someden/export.csv')
