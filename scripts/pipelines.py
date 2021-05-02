# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import gzip
from scrapy.exporters import CsvItemExporter
from scrapy import signals
from pydispatch import dispatcher
from .items import (DistrictItem, BlockItem, PanchayatItem, VillageItem, FPSItem, RationCardItem,
                    RationCardDataItem, RationCardFamilyItem, RationCardTransactionItem,
                    NagarpalikaItem, WardItem, UrbanFPSItem, UrbanRationCardItem,
                    UrbanRationCardDataItem, UrbanRationCardFamilyItem, UrbanRationCardTransactionItem)

def item_type(item):
    return type(item).__name__.replace('Item','').lower()  # TeamItem => team

class RationPipeline(object):
    SaveTypes = ['district', 'block', 'panchayat', 'village', 'fps', 'rationcard',
                 'rationcarddata', 'rationcardfamily', 'rationcardtransaction',
                 'nagarpalika', 'ward', 'urbanfps', 'urbanrationcard',
                 'urbanrationcarddata', 'urbanrationcardfamily', 'urbanrationcardtransaction']

    def __init__(self):
        dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    def spider_opened(self, spider):
        self.files = dict([ (name, gzip.open(name+'.csv.gz','w+b')) for name in self.SaveTypes ])
        self.exporters = dict([ (name,CsvItemExporter(self.files[name])) for name in self.SaveTypes])
        self.exporters['district'].fields_to_export = DistrictItem.fields_to_export
        self.exporters['block'].fields_to_export = BlockItem.fields_to_export
        self.exporters['panchayat'].fields_to_export = PanchayatItem.fields_to_export
        self.exporters['village'].fields_to_export = VillageItem.fields_to_export
        self.exporters['fps'].fields_to_export = FPSItem.fields_to_export
        self.exporters['rationcard'].fields_to_export = RationCardItem.fields_to_export
        self.exporters['rationcarddata'].fields_to_export = RationCardDataItem.fields_to_export
        self.exporters['rationcardfamily'].fields_to_export = RationCardFamilyItem.fields_to_export
        self.exporters['rationcardtransaction'].fields_to_export = RationCardTransactionItem.fields_to_export
        self.exporters['nagarpalika'].fields_to_export = NagarpalikaItem.fields_to_export
        self.exporters['ward'].fields_to_export = WardItem.fields_to_export
        self.exporters['urbanfps'].fields_to_export = UrbanFPSItem.fields_to_export
        self.exporters['urbanrationcard'].fields_to_export = UrbanRationCardItem.fields_to_export
        self.exporters['urbanrationcarddata'].fields_to_export = UrbanRationCardDataItem.fields_to_export
        self.exporters['urbanrationcardfamily'].fields_to_export = UrbanRationCardFamilyItem.fields_to_export
        self.exporters['urbanrationcardtransaction'].fields_to_export = UrbanRationCardTransactionItem.fields_to_export
        [e.start_exporting() for e in self.exporters.values()]

    def spider_closed(self, spider):
        [e.finish_exporting() for e in self.exporters.values()]
        [f.close() for f in self.files.values()]

    def process_item(self, item, spider):
        what = item_type(item)
        if what in set(self.SaveTypes):
            self.exporters[what].export_item(item)
        return item
