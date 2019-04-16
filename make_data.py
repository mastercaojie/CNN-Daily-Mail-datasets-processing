import os
import argparse

SENTENCE_START = '<s>'
SENTENCE_END = '</s>'
dm_single_close_quote = u'\u2019' # unicode
dm_double_close_quote = u'\u201d'
END_TOKENS = ['.', '!', '?', '...', "'", "`", '"', dm_single_close_quote, dm_double_close_quote, ")"]


def read_text_file(text_file):
    lines = []
    with open(text_file, "r",encoding='utf8') as f:
        for line in f:
            lines.append(line.strip())
    return lines

def fix_missing_period(line):
    if "@highlight" in line: return line
    if line=="": return line
    if line[-1] in END_TOKENS: return line
  # print line[-1]
    return line + " ."

def get_art_abs(story_file):
    lines = read_text_file(story_file)
    # Lowercase everything
    lines = [line.lower() for line in lines]
    # Put periods on the ends of lines that are missing them (this is a problem in the dataset because many image captions don't end in periods; consequently they end up in the body of the article as run-on sentences)
    lines = [fix_missing_period(line) for line in lines]
    # Separate out article and abstract sentences
    article_lines = []
    highlights = []
    next_is_highlight = False
    for idx, line in enumerate(lines):
        if line == "":
            continue # empty line
        elif line.startswith("@highlight"):
            next_is_highlight = True
        elif next_is_highlight:
            highlights.append(line)
        else:
            article_lines.append(line)
    # Make article into a single string
    article = ' '.join(article_lines)
    # Make abstract into a signle string, putting <s> and </s> tags around the sentences
    #abstract = ' '.join(["%s %s %s" % (SENTENCE_START, sent, SENTENCE_END) for sent in highlights])
    abstract = ' '.join(highlights)
    return article, abstract

def get_paths(ospath):
    print(ospath)
    """Get all textgrid files form the path"""
    tgrid = []
    for path, d, filelist in os.walk(ospath):
        for filename in filelist:
            d = os.path.join(path, filename)
            if d.endswith(".story"):
                tgrid.append(d)
    tgrid.sort()
    return tgrid

def main(input_path, output_path):
    filenames = get_paths(input_path)
    for file_name in filenames:
        article, abstract = get_art_abs(file_name)
        with open(output_path + 'train.src', 'a+', encoding='utf8') as fs,\
                open(output_path + 'train.tgt', 'a+',encoding='utf8')as ft:
            ft.write(abstract+'\n')
            fs.write(article + '\n')
        #print(abstract)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_path',# default='data',
                        help='Input data file path, Example: path/cnn/stories')
    parser.add_argument('-o', '--output_path', #default='result',
                        help='Stored result file path;Example: path/cnn/train')
    args = parser.parse_args()
    print('start processing.......')
    main(args.input_path,args.output_path)
    print('Processing completed!')



