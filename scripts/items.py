# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import json    
from collections import OrderedDict


class OrderedItem(scrapy.Item):
    def __init__(self, *args, **kwargs):
        self._values = OrderedDict()
        if args or kwargs:
            for k, v in six.iteritems(dict(*args, **kwargs)):
                self[k] = v

    def __repr__(self):
        return json.dumps(OrderedDict(self),ensure_ascii = False)  
        #ensure_ascii = False ,it make characters show in cjk appearance.


class DistrictItem(OrderedItem):
    fields_to_export = ['S_No', 'District', 'Rural', 'Urban', 'Annapurna', 'Antoydaya', 'Below_Poverty_Line', 'State_BPL', 'Others', 'Total', 'District_Code']
    S_No = scrapy.Field()
    District = scrapy.Field()
    Rural = scrapy.Field()
    Urban = scrapy.Field()
    Annapurna = scrapy.Field()
    Antoydaya = scrapy.Field()
    Below_Poverty_Line = scrapy.Field()
    State_BPL = scrapy.Field()
    Others = scrapy.Field()
    Total = scrapy.Field()
    District_Code = scrapy.Field()


class BlockItem(OrderedItem):
    fields_to_export = ['S_No', 'Block', 'Annapurna', 'Antoydaya', 'Below_Poverty_Line', 'State_BPL', 'Others', 'Total', 'Block_Code', 'District_Code']
    S_No = scrapy.Field()
    Block = scrapy.Field()
    Annapurna = scrapy.Field()
    Antoydaya = scrapy.Field()
    Below_Poverty_Line = scrapy.Field()
    State_BPL = scrapy.Field()
    Others = scrapy.Field()
    Total = scrapy.Field()
    Block_Code = scrapy.Field()
    District_Code = scrapy.Field()


class PanchayatItem(OrderedItem):
    fields_to_export = ['S_No', 'Panchayat', 'Annapurna', 'Antoydaya', 'Below_Poverty_Line', 'State_BPL', 'Others', 'Total', 'Panchayat_Code', 'Block_Code', 'District_Code']
    S_No = scrapy.Field()
    Panchayat = scrapy.Field()
    Annapurna = scrapy.Field()
    Antoydaya = scrapy.Field()
    Below_Poverty_Line = scrapy.Field()
    State_BPL = scrapy.Field()
    Others = scrapy.Field()
    Total = scrapy.Field()
    Panchayat_Code = scrapy.Field()
    District_Code = scrapy.Field()
    Block_Code = scrapy.Field()


class VillageItem(OrderedItem):
    fields_to_export = ['S_No', 'Village', 'Annapurna', 'Antoydaya', 'Below_Poverty_Line', 'State_BPL', 'Others', 'Total', 'Village_Code', 'Panchayat_Code', 'Block_Code', 'District_Code', ]
    S_No = scrapy.Field()
    Village = scrapy.Field()
    Annapurna = scrapy.Field()
    Antoydaya = scrapy.Field()
    Below_Poverty_Line = scrapy.Field()
    State_BPL = scrapy.Field()
    Others = scrapy.Field()
    Total = scrapy.Field()
    Village_Code = scrapy.Field()
    Panchayat_Code = scrapy.Field()
    District_Code = scrapy.Field()
    Block_Code = scrapy.Field()


class FPSItem(OrderedItem):
    fields_to_export = ['S_No', 'FPS_Name', 'Annapurna', 'Antoydaya', 'Below_Poverty_Line', 'State_BPL', 'Others', 'Total', 'FPS_Code', 'Village_Code', 'Panchayat_Code', 'Block_Code', 'District_Code']
    S_No = scrapy.Field()
    FPS_Name = scrapy.Field()
    Annapurna = scrapy.Field()
    Antoydaya = scrapy.Field()
    Below_Poverty_Line = scrapy.Field()
    State_BPL = scrapy.Field()
    Others = scrapy.Field()
    Total = scrapy.Field()
    FPS_Code = scrapy.Field()
    Village_Code = scrapy.Field()
    Panchayat_Code = scrapy.Field()
    Block_Code = scrapy.Field()
    District_Code = scrapy.Field()


class RationCardItem(OrderedItem):
    fields_to_export = ['S_No', 'Ration_Card_Number', 'Card_Type', 'Applicant_Name', 'Father_Name', 'Address', 'Number_of_Family_Members', 'District_Code', 'Block_Code', 'Panchayat_Code', 'Village_Code', 'FPS_Code']
    S_No = scrapy.Field()
    Ration_Card_Number = scrapy.Field()
    Card_Type = scrapy.Field()
    Applicant_Name = scrapy.Field()
    Father_Name = scrapy.Field()
    Address = scrapy.Field()
    Number_of_Family_Members = scrapy.Field()
    District_Code = scrapy.Field()
    Block_Code = scrapy.Field()
    Panchayat_Code = scrapy.Field()
    Village_Code = scrapy.Field()
    FPS_Code = scrapy.Field()


class RationCardDataItem(OrderedItem):
    # primary_consumer_name: consumer_photo: store path to the photo of the image in the field + image address_2: mobile_number: shop_name: gas_type:
    fields_to_export = ['Ration_Card_Number', 'Card_Type', 'Type_of_Food_Safety', 'Consumer_Name', 'Address', 'Mobile_Number', 'Name_of_Fair_Price_Shopkeeper', 'Gas_Type', 'Gas_Agency', 'Consumer_Number', 'Photo_Path']
    Ration_Card_Number = scrapy.Field()
    Card_Type = scrapy.Field()
    Type_of_Food_Safety = scrapy.Field()
    Consumer_Name = scrapy.Field()
    Address = scrapy.Field()
    Mobile_Number = scrapy.Field()
    Name_of_Fair_Price_Shopkeeper = scrapy.Field()
    Gas_Type = scrapy.Field()
    Gas_Agency = scrapy.Field()
    Consumer_Number = scrapy.Field()
    Photo_Path = scrapy.Field()


class RationCardFamilyItem(OrderedItem):
    # ration_card_sno: ration_card_consumer_name: ration_card_age: ration_card_fathers_name: ration_card_relationship_with_primary_consumer:
    fields_to_export = ['Ration_Card_Number', 'S_No', 'Consumer_Name', 'Age', 'Father_Name', 'Relationship']
    Ration_Card_Number = scrapy.Field()
    S_No = scrapy.Field()
    Consumer_Name = scrapy.Field()
    Age = scrapy.Field()
    Father_Name = scrapy.Field()
    Relationship = scrapy.Field()


class RationCardTransactionItem(OrderedItem):
    # bill_number: bill_date: shop_name: items: amount:
    fields_to_export = ['Ration_Card_Number', 'Bill_Number', 'Bill_Date', 'Shop_Name', 'Type_of_Food', 'Quantity_of_Food']
    Ration_Card_Number = scrapy.Field()
    Bill_Number = scrapy.Field()
    Bill_Date = scrapy.Field()
    Shop_Name = scrapy.Field()
    Type_of_Food = scrapy.Field()
    Quantity_of_Food = scrapy.Field()


class NagarpalikaItem(OrderedItem):
    fields_to_export = ['S_No', 'Nagarpalika', 'Annapurna', 'Antoydaya', 'Below_Poverty_Line', 'State_BPL', 'Others', 'Total', 'Nagarpalika_Code', 'District_Code']
    S_No = scrapy.Field()
    Nagarpalika = scrapy.Field()
    Annapurna = scrapy.Field()
    Antoydaya = scrapy.Field()
    Below_Poverty_Line = scrapy.Field()
    State_BPL = scrapy.Field()
    Others = scrapy.Field()
    Total = scrapy.Field()
    Nagarpalika_Code = scrapy.Field()
    District_Code = scrapy.Field()


class WardItem(OrderedItem):
    fields_to_export = ['S_No', 'Ward', 'Annapurna', 'Antoydaya', 'Below_Poverty_Line', 'State_BPL', 'Others', 'Total', 'Ward_Code', 'Nagarpalika_Code', 'District_Code']
    S_No = scrapy.Field()
    Ward = scrapy.Field()
    Annapurna = scrapy.Field()
    Antoydaya = scrapy.Field()
    Below_Poverty_Line = scrapy.Field()
    State_BPL = scrapy.Field()
    Others = scrapy.Field()
    Total = scrapy.Field()
    Ward_Code = scrapy.Field()
    Nagarpalika_Code = scrapy.Field()
    District_Code = scrapy.Field()


class UrbanFPSItem(OrderedItem):
    fields_to_export = ['S_No', 'FPS_Name', 'Annapurna', 'Antoydaya', 'Below_Poverty_Line', 'State_BPL', 'Others', 'Total', 'FPS_Code', 'Ward_Code', 'Nagarpalika_Code', 'District_Code']
    S_No = scrapy.Field()
    FPS_Name = scrapy.Field()
    Annapurna = scrapy.Field()
    Antoydaya = scrapy.Field()
    Below_Poverty_Line = scrapy.Field()
    State_BPL = scrapy.Field()
    Others = scrapy.Field()
    Total = scrapy.Field()
    FPS_Code = scrapy.Field()
    Ward_Code = scrapy.Field()
    Nagarpalika_Code = scrapy.Field()
    District_Code = scrapy.Field()


class UrbanRationCardItem(OrderedItem):
    fields_to_export = ['S_No', 'Ration_Card_Number', 'Card_Type', 'Applicant_Name', 'Father_Name', 'Address', 'Number_of_Family_Members', 'District_Code', 'Nagarpalika_Code', 'Ward_Code', 'FPS_Code']
    S_No = scrapy.Field()
    Ration_Card_Number = scrapy.Field()
    Card_Type = scrapy.Field()
    Applicant_Name = scrapy.Field()
    Father_Name = scrapy.Field()
    Address = scrapy.Field()
    Number_of_Family_Members = scrapy.Field()
    District_Code = scrapy.Field()
    Nagarpalika_Code = scrapy.Field()
    Ward_Code = scrapy.Field()
    FPS_Code = scrapy.Field()


class UrbanRationCardDataItem(OrderedItem):
    # primary_consumer_name: consumer_photo: store path to the photo of the image in the field + image address_2: mobile_number: shop_name: gas_type:
    fields_to_export = ['Ration_Card_Number', 'Card_Type', 'Type_of_Food_Safety', 'Consumer_Name', 'Address', 'Mobile_Number', 'Name_of_Fair_Price_Shopkeeper', 'Gas_Type', 'Gas_Agency', 'Consumer_Number', 'Photo_Path']
    Ration_Card_Number = scrapy.Field()
    Card_Type = scrapy.Field()
    Type_of_Food_Safety = scrapy.Field()
    Consumer_Name = scrapy.Field()
    Address = scrapy.Field()
    Mobile_Number = scrapy.Field()
    Name_of_Fair_Price_Shopkeeper = scrapy.Field()
    Gas_Type = scrapy.Field()
    Gas_Agency = scrapy.Field()
    Consumer_Number = scrapy.Field()
    Photo_Path = scrapy.Field()


class UrbanRationCardFamilyItem(OrderedItem):
    # ration_card_sno: ration_card_consumer_name: ration_card_age: ration_card_fathers_name: ration_card_relationship_with_primary_consumer:
    fields_to_export = ['Ration_Card_Number', 'S_No', 'Consumer_Name', 'Age', 'Father_Name', 'Relationship']
    Ration_Card_Number = scrapy.Field()
    S_No = scrapy.Field()
    Consumer_Name = scrapy.Field()
    Age = scrapy.Field()
    Father_Name = scrapy.Field()
    Relationship = scrapy.Field()


class UrbanRationCardTransactionItem(OrderedItem):
    # bill_number: bill_date: shop_name: items: amount:
    fields_to_export = ['Ration_Card_Number', 'Bill_Number', 'Bill_Date', 'Shop_Name', 'Type_of_Food', 'Quantity_of_Food']
    Ration_Card_Number = scrapy.Field()
    Bill_Number = scrapy.Field()
    Bill_Date = scrapy.Field()
    Shop_Name = scrapy.Field()
    Type_of_Food = scrapy.Field()
    Quantity_of_Food = scrapy.Field()
