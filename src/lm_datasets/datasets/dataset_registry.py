from typing import List, Optional, Union
from .multilingual.wikimedia import get_wikimedia_auto_classes
from .multilingual.colossal_oscar import get_colossal_oscar_auto_classes
from .multilingual.eurlex import get_eurlex_auto_classes
from .multilingual.legal_mc4 import get_legal_mc4_auto_classes
from .fr.pleiasnews import get_pleias_news_auto_classes
from .fr.pleiasbooks import get_pleias_books_auto_classes
from .code.starcoder import get_auto_starcoder_classes
from .nl.sonar import get_sonar_classes
from .en.pile_of_law import get_pile_of_law_auto_classes
import importlib
import logging


logger = logging.getLogger(__name__)


ALL_DATASET_IMPORTS = [
    # multilingual
    # curlicat
    ".multilingual.curlicat.CurlicatBGDataset",
    ".multilingual.curlicat.CurlicatHRDataset",
    ".multilingual.curlicat.CurlicatHUDataset",
    ".multilingual.curlicat.CurlicatPLDataset",
    ".multilingual.curlicat.CurlicatRODataset",
    ".multilingual.curlicat.CurlicatSKDataset",
    ".multilingual.curlicat.CurlicatSLDataset",
    # macocu
    ".multilingual.macocu.MacocuBGDataset",
    ".multilingual.macocu.MacocuHRDataset",
    ".multilingual.macocu.MacocuELDataset",
    # ".multilingual.macocu.MacocuSQDataset",
    # ".multilingual.macocu.MacocuBSDataset",
    ".multilingual.macocu.MacocuCADataset",
    # ".multilingual.macocu.MacocuISDataset",
    # ".multilingual.macocu.MacocuMKDataset",
    ".multilingual.macocu.MacocuMTDataset",
    # ".multilingual.macocu.MacocuCNRDataset",
    ".multilingual.macocu.MacocuSRDataset",
    ".multilingual.macocu.MacocuSLDataset",
    # ".multilingual.macocu.MacocuTRDataset",
    ".multilingual.macocu.MacocuUKDataset",
    # redpajama
    ".multilingual.redpajama.RedPajamaBookDataset",
    # ".multilingual.redpajama.RedPajamaArxivDataset",
    ".multilingual.redpajama.RedPajamaStackexchangeDataset",
    ".multilingual.wura.WuraENDataset",
    ".multilingual.wura.WuraFRDataset",
    ".multilingual.wura.WuraPTDataset",
    ".multilingual.wura.WuraAFDataset",
    ".multilingual.wura.WuraAMDataset",
    ".multilingual.wura.WuraHADataset",
    ".multilingual.wura.WuraARDataset",
    ".multilingual.wura.WuraIGDataset",
    ".multilingual.wura.WuraRWDataset",
    ".multilingual.wura.WuraMGDataset",
    ".multilingual.wura.WuraNYDataset",
    ".multilingual.wura.WuraOMDataset",
    ".multilingual.wura.WuraSNDataset",
    ".multilingual.wura.WuraSODataset",
    ".multilingual.wura.WuraSTDataset",
    ".multilingual.wura.WuraSWDataset",
    ".multilingual.wura.WuraTIDataset",
    ".multilingual.wura.WuraXHDataset",
    ".multilingual.wura.WuraYODataset",
    ".multilingual.wura.WuraZUDataset",
    # en
    ".en.wikihow.WikihowDataset",
    ".en.pes2o.PeS2oDataset",
    ".en.proof_pile.ProofPileDataset",
    ".en.dialogstudio.DialogstudioDataset",
    ".en.pile_of_law.PileOfLawDataset",
    ".en.math_amps.MathAMPSDataset",
    ".en.edgar.EdgarCorpus",
    # bg
    # ".bg.bgnc_admin_eur.BGNCAdminEURDataset",  # deprecated -> use bulnc
    # ".bg.bgnc_news_corpus.BGNCNewsCorpusDataset",  # deprecated -> use bulnc
    ".bg.bulgarian_news.BulgarianNewsDataset",
    ".bg.bulnc.BulNCDataset",
    # de
    ".de.openlegaldata.OpenLegalDataDataset",
    ".de.dewac.DEWacDataset",
    # ga
    ".ga.ga_bilingual_legistation.GABilingualLegislationDataset",
    ".ga.ga_universal_dependencies.GAUniversalDependenciesDataset",
    # hr
    ".hr.hrwac.HRWACDataset",
    ".hr.styria_news.StyriaNewsDataset",
    ".hr.croatian_news_engri.CroatianNewsENGRIDataset",
    # it
    ".it.itwac.ITWacDataset",
    ".it.gazzetta_ufficiale.GazzettaUfficiale"
    # mt
    ".mt.korpus_malti.KorpusMaltiDataset",
    # nl
    *get_sonar_classes(),
    ".nl.sonar_new_media.SonarNewMediaDataset",
    # sl
    ".sl.cc_gigafida.CCGigaFidaDataset",
    ".sl.academic_slovene_kas.AcademicSloveneKASDataset",
    ".sl.slwac_web.SLWaCWebDataset",
    # sk
    ".sk.sk_court_decisions.SKCourtDecisionsDataset",
    ".sk.sk_laws.SKLawsDataset",
    # cs
    ".cs.syn_v9.SynV9Dataset",
    ".cs.cs_en_parallel.CzechEnglishParallelDataset",
    # da
    ".da.danish_gigaword.DanishGigawordDataset",
    # danish_parliament_corpus.DanishParliamentCorpusDataset,
    ".da.danewsroom.DANewsroomDataset",
    ".da.dk_clarin.DKClarinDataset",
    # fr
    ".fr.cabernet.CaBeRnetDataset",
    # no
    ".no.norwegian_cc.NorwegianCCNNDataset",
    ".no.norwegian_cc.NorwegianCCNODataset",
    # nak.NAKDataset,
    # nbdigital.NBDigitalDataset,
    # maalfrid_2021.Maalfrid2021Dataset,
    # parlamint.ParlaMintDataset,
    # parliamentary_proceedings.ParliamentaryProceedingsDataset,
    # sakspapir_nno.SakspapirNNODataset,
    # pl
    # ".pl.luna_pl.LunaPL",  ### BAD data
    ".pl.pl_nkjp.NKJPPodkorpusMilionowyDataset",
    ".pl.pl_parliamentary_corpus.PLParliamentaryCorpusDataset",
    # pt
    ".pt.parlamento_pt.ParlamentoPtDataset",
    ".pt.brwac.BrWacDataset",
    # lt
    ".lt.seimas_lt_en.SeismasLTENDataset",
    # lv
    ".lv.state_related_latvian_web.StateRelatedLatvianWebDataset",
    # el
    ".el.greek_legal_code.GreekLegalCodeDataset",
    ".el.greek_web_corpus.GreekWebCorpus",
    # et
    ".et.estonian_reference_corpus.EstonianReferenceCorpusDataset",
    ".et.enc.ENC2021Dataset",
    ".et.ekspress.EkspressDataset",
    # eu
    ".eu.euscrawl.EUSCrawlDataset",
    ".eu.euscrawl.EUSCrawlFilteredDataset",
    # es
    ".es.spanish_legal.SpanishLegalDataset",
    # ".es.escorpius.ESCorpiusDataset",  # based on CC => use OSCAR instead
    # fi
    ".fi.ylenews.YLENewsDataset",
    # sv
    ".sv.sv_gigaword.SVGigawordDataset",
    # sr
    ".sr.srpkor.SrpKorDataset",
    # ro
    ".ro.marcell_legislative_subcorpus_v2.MarcellLegislativeSubcorpusV2Dataset",
    # uk
    ".uk.uk_laws.UKLawsDataset",
]


def get_class_by_import_string(
    import_string_or_cls: Union[str, object], relative_base_package: str = "lm_datasets.datasets"
):
    """
    Import dataset class based on import string

    Allowed formats:
    - ".lang.DatasetClass"   # relative
    - "lm_datasets.lang.DatasetClass"  # absolute
    """

    if isinstance(import_string_or_cls, str):
        # import from string
        if import_string_or_cls.startswith("."):  # relative import
            package = relative_base_package
        else:
            package = None  # absolute

        import_split = import_string_or_cls.split(".")
        cls_name = import_split[-1]
        mod_str = ".".join(import_split[:-1])

        mod = importlib.import_module(mod_str, package=package)

        return getattr(mod, cls_name)
    else:
        return import_string_or_cls  # already object, no need to import from string


def get_registered_dataset_classes(
    extra_dataset_registries: Optional[Union[str, List[str]]] = None,
    extra_dataset_classes: Optional[List] = None,
    use_default_registry: bool = True,
):
    """
    Construct list of registered dataset classes
    """
    dataset_classes = []

    # Predefined dataset classes (default registry)
    if use_default_registry:
        dataset_classes += (
            [get_class_by_import_string(clss) for clss in ALL_DATASET_IMPORTS]
            + get_eurlex_auto_classes()
            + get_legal_mc4_auto_classes()
            + get_wikimedia_auto_classes()
            + get_colossal_oscar_auto_classes()
            + get_auto_starcoder_classes()
            + get_pile_of_law_auto_classes()
            + get_pleias_news_auto_classes()
            + get_pleias_books_auto_classes()
        )

    if extra_dataset_classes:
        dataset_classes += extra_dataset_classes

    # Load dataset classes from extra registries
    if extra_dataset_registries:
        if isinstance(extra_dataset_registries, str):
            extra_dataset_registries = extra_dataset_registries.split(",")

        # Iterate over registeries
        for extra_dataset_registry_str in extra_dataset_registries:
            logger.info(f"Loading datasets from registry: {extra_dataset_registry_str}")
            extra_dataset_registry_package = importlib.import_module(extra_dataset_registry_str)

            extra_dataset_registry_getter = getattr(extra_dataset_registry_package, "get_registered_dataset_classes")
            extra_dataset_classes_from_registry = extra_dataset_registry_getter()

            logger.debug(f"Extra datasets: {extra_dataset_classes_from_registry}")

            dataset_classes += extra_dataset_classes_from_registry

    return dataset_classes


def get_registered_dataset_ids(
    extra_dataset_registries: Optional[Union[str, List[str]]] = None, needed_source_id: Optional[str] = None
):
    return [
        cls.DATASET_ID
        for cls in get_registered_dataset_classes(extra_dataset_registries)
        if needed_source_id is None or cls.SOURCE_ID == needed_source_id
    ]


def get_dataset_class_by_id(dataset_id, extra_dataset_registries: Optional[Union[str, List[str]]] = None):
    id_to_dataset_class = {cls.DATASET_ID: cls for cls in get_registered_dataset_classes(extra_dataset_registries)}

    if dataset_id in id_to_dataset_class:
        dataset_cls = id_to_dataset_class[dataset_id]
    else:
        raise ValueError(f"Unknown dataset ID: {dataset_id} (available: {id_to_dataset_class.keys()})")

    dataset_cls = id_to_dataset_class[dataset_id]

    return dataset_cls
