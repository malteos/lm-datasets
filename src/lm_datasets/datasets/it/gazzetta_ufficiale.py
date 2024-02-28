from lm_datasets.datasets.base import Availability, GB, License
from lm_datasets.datasets.hf_dataset import HFDataset


class GazzettaUfficiale(HFDataset):
    DATASET_ID = "gazzetta-ufficiale"

    TITLE = "Gazzeta Ufficiale"
    HOMEPAGE = "https://huggingface.co/datasets/mii-llm/gazzetta-ufficiale"
    # LICENSE = # not specified on HF page
    AVAILABILITY = Availability.DIRECT_DOWNLOAD
    LANGUAGES = ["it"]
    DESCRIPTION = """La Gazzetta Ufficiale della Repubblica Italiana, quale fonte ufficiale di conoscenza
    delle norme in vigore in Italia e strumento di diffusione, informazione e ufficializzazione di
    testi legislativi, atti pubblici e privati, è edita dall’Istituto Poligrafico e Zecca dello
    Stato e pubblicata in collaborazione con il Ministero della Giustizia, il quale provvede alla direzione e redazione della stessa.
    L'Istituto Poligrafico e Zecca dello Stato S.p.A. promuove la più ampia fruibilità della Gazzetta
    Ufficiale della Repubblica Italiana in formato digitale.
    Si segnala che l'unico testo definitivo è quello pubblicato sulla Gazzetta Ufficiale a mezzo stampa,
    che prevale in caso di discordanza. La riproduzione dei testi forniti nel formato elettronico è consentita purché venga menzionata la fonte, il carattere non autentico e gratuito.
    """

    HF_DATASET_ID = "mii-llm/gazzetta-ufficiale"
    HF_DATASET_CONFIGS = ["default"]
    HF_DATASET_SPLIT = "train"
    keep_columns = True

    def get_text_from_item(self, item) -> str:
        """
        Subscribing the original method since this dataset
        has multiple columns.

        Iterates over the row columns and concatenates the columns content
        item: <dict:{column_name: content}>
        """
        txt = ""
        txt_colums = ['text', 'field1', 'field2', 'about']
        for column in txt_colums:
            txt += item[column]
        return txt
