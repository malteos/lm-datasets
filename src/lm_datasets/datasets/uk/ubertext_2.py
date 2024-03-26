from lm_datasets.datasets.base import BaseDataset, Availability
import bz2
import os
import chardet


class UberText2(BaseDataset):
    DATASET_ID = "ubertext2"
    # SOURCE_ID =
    TITLE = "UberText2.0"
    # DESCRIPTION =
    HOMEPAGE = "https://lang.org.ua/en/ubertext/"
    AVAILIBILITY = Availability.DIRECT_DOWNLOAD.name
    DOWNLOAD_URLS = ["https://lang.org.ua/static/downloads/ubertext2.0/court/based/ubertext.court.filter_rus_gcld+short.text_only.txt.bz2",
                     "https://lang.org.ua/static/downloads/ubertext2.0/fiction/based/ubertext.fiction.filter_rus_gcld+short.text_only.txt.bz2",
                     "https://lang.org.ua/static/downloads/ubertext2.0/news/based/ubertext.news.filter_rus_gcld+short.text_only.txt.bz2",
                     "https://lang.org.ua/static/downloads/ubertext2.0/social/based/ubertext.social.filter_rus_gcld+short.text_only.txt.bz2",
                     "https://lang.org.ua/static/downloads/ubertext2.0/wikipedia/based/ubertext.wikipedia.filter_rus_gcld+short.text_only.txt.bz2"]

    DOI = "https://doi.org/10.18653/v1/2023.unlp-1.1"
    CITATION = """@inproceedings{chaplynskyi-2023-introducing,
            title = "Introducing {U}ber{T}ext 2.0: A Corpus of Modern {U}krainian at Scale",
            author = "Chaplynskyi, Dmytro",
            booktitle = "Proceedings of the Second Ukrainian Natural Language Processing Workshop",
            month = may,
            year = "2023",
            address = "Dubrovnik, Croatia",
            publisher = "Association for Computational Linguistics",
            url = "https://aclanthology.org/2023.unlp-1.1",
            pages = "1--10",
            }"""
    LANGUAGES = ["uk"]

    def extract_txt_file(self):
        output = self.get_local_dataset_dir()
        bz2_files = ["ubertext.court.filter_rus_gcld+short.text_only.txt.bz2",
                     "ubertext.fiction.filter_rus_gcld+short.text_only.txt.bz2",
                     "ubertext.news.filter_rus_gcld+short.text_only.txt.bz2",
                     "ubertext.social.filter_rus_gcld+short.text_only.txt.bz2",
                     "ubertext.wikipedia.filter_rus_gcld+short.text_only.txt.bz2"]
        # Decompressor object
        decompressor = bz2.BZ2Decompressor()
        output_txt = output + "/ubertext.txt"
        print("Writing to {}".format(output_txt))
        for bz2_file in bz2_files:
            with bz2.BZ2File(os.path.join(output, bz2_file), "rb") as f, open(output_txt, 'ab') as out_f:
                # Decompress data from file
                print("decompressing from: {}".format(bz2_file))
                for data in iter(lambda: f.read(100 * 1024), b''):
                    # yield bz2.decompress(f.read())
                    out_f.write(data)
                    out_f.write(b'\n')
                # yield (bz2.decompress(f.read()))

    def get_texts(self):
        output_txt = self.get_local_dataset_dir() + "/ubertext.txt"
        print('read into local dateset')
        with open(output_txt, "r", encoding='utf-32') as f:
            print('read file')
            for line in f.readlines():
                yield line
            # for line in f.readlines():

            # print(chardet.detect(line))
            # yield line.decode('ascii')
            # yield line
