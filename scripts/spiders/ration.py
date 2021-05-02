# -*- coding: utf-8 -*-

import time
import os
import re
import gzip
from base64 import b64decode
import pandas as pd

import scrapy
from scrapy.http import FormRequest

from ..items import (DistrictItem, BlockItem, PanchayatItem, VillageItem, FPSItem, RationCardItem,
                     RationCardDataItem, RationCardFamilyItem, RationCardTransactionItem,
                     NagarpalikaItem, WardItem, UrbanFPSItem, UrbanRationCardItem,
                     UrbanRationCardDataItem, UrbanRationCardFamilyItem, UrbanRationCardTransactionItem)


class RationNewsSpider(scrapy.Spider):
    #download_delay = 1
    name = 'ration'
    allowed_domains = ['food.raj.nic.in']
    start_urls = ['https://food.raj.nic.in/DistrictWiseCategoryDetails.aspx']

    def save_gzip_file(self, response, filename):
        fn = filename + '.gz'
        with gzip.open(fn, 'wb') as f:
            f.write(response.body)
        self.log('Saved file {}'.format(fn) )
        return fn

    def parse(self, response):
        """
            How to pass argument to spider:-
            arg = getattr(self, 'arg', None)
        """
        if not os.path.exists('./html'):
            os.makedirs('./html')
        if not os.path.exists('./html/rural'):
            os.makedirs('./html/rural')
        if not os.path.exists('./html/urban'):
            os.makedirs('./html/urban')
        page = response.meta.get('page', 0)
        cookiejar = response.meta.get('cookiejar', None)

        filter = getattr(self, 'filter', 'all')
        districts = getattr(self, 'districts', None)
        detail = getattr(self, 'detail', 'no')
        if districts:
            s_no_list = ['{:s}.'.format(a.strip()) for a in districts.split(',')]
        print('Arguments: filter={!s}, districts={!s}, detail={!s}'.format(filter, districts, detail))
        if filter in ['all', 'rural']:
            for i, href in enumerate(response.xpath("//a[re:test(@id, 'grdDistrict_lnkRural_\d+$')]")):
                item = DistrictItem()
                item['District_Code'] = href.xpath("../..//input[@id='grdDistrict_hdnDistrictCode_%d']/@value" % i).extract()[0].strip()
                for j, col in enumerate(href.xpath('../../td')):
                    val = ''.join(col.xpath('.//text()').extract())
                    item[DistrictItem.fields_to_export[j]] = val.strip()
                yield item
                if districts:
                    if item['S_No'] not in s_no_list:
                        continue
                url = href.attrib['href']
                m = re.match(".*?\((.*?)\,(.*?)\)", url)
                if m:
                    target = m.group(1).replace("'", "")
                    arg = m.group(2).replace("'", "")
                    yield FormRequest.from_response(response,
                        formdata={'__EVENTTARGET': target, '__EVENTARGUMENT': arg},
                        callback = self.parse_rural,
                        dont_click = True,
                        dont_filter = True,
                        meta={'src': 'rural', 'fork_from_cookiejar': cookiejar, 'cookiejar': str(page * 1000 + i + 1)})
                #break

        if filter in ['all', 'urban']:
            for i, href in enumerate(response.xpath("//a[re:test(@id, 'grdDistrict_lnkUrban_\d+$')]")):
                if filter == 'urban':
                    item = DistrictItem()
                    item['District_Code'] = href.xpath("../..//input[@id='grdDistrict_hdnDistrictCode_%d']/@value" % i).extract()[0].strip()
                    for j, col in enumerate(href.xpath('../../td')):
                        val = ''.join(col.xpath('.//text()').extract())
                        item[DistrictItem.fields_to_export[j]] = val.strip()
                    yield item
                if districts:
                    if item['S_No'] not in s_no_list:
                        continue
                url = href.attrib['href']
                m = re.match(".*?\((.*?)\,(.*?)\)", url)
                if m:
                    target = m.group(1).replace("'", "")
                    arg = m.group(2).replace("'", "")
                    yield FormRequest.from_response(response,
                        formdata={'__EVENTTARGET': target, '__EVENTARGUMENT': arg},
                        callback = self.parse_urban,
                        dont_click = True,
                        dont_filter = True,
                        meta={'src': 'urban', 'fork_from_cookiejar': cookiejar, 'cookiejar': str(page * 1000 + 100 + i + 1)})

        href = response.xpath("//a/font[.='Next']/..")
        if len(href):
            url = href[0].attrib['href']
            m = re.match(".*?\((.*?)\,(.*?)\)", url)
            if m:
                target = m.group(1).replace("'", "")
                arg = m.group(2).replace("'", "")
                print('********* NEXT DISTRICT *********', target, arg)
                page += 1
                yield FormRequest.from_response(response,
                    formdata={'__EVENTTARGET': target, '__EVENTARGUMENT': arg},
                    callback = self.parse,
                    dont_click = True,
                    meta={'page': page, 'fork_from_cookiejar': cookiejar, 'cookiejar': str(page * 1000)})

    def parse_detail(self, response):
        self.log('<<<<<<<<<<<<<<<<<<<<<<<Detail URL %s (meta=%r)' % (response.url, response.meta))
        #gen = response.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").extract()[0]
        #state = response.xpath("//input[@id='__VIEWSTATE']/@value").extract()[0]
        #print(gen, len(state))
        item = response.meta.get('item')
        card_no = item['Ration_Card_Number'].strip()
        if type(item).__name__ == 'RationCardItem':
            dst = 'rural'
            item = RationCardDataItem()
        else:
            dst ='urban'
            item = UrbanRationCardDataItem()
        # FIXME: Don't save
        #filename = './html/%s/%s.html' % (dst, card_no)
        #self.save_gzip_file(response, filename)
        app_name = response.xpath("//span[@id='lblApplicantName']/text()").extract()
        card_type = response.xpath("//span[@id='lblCardType']/text()").extract()
        nfsa = response.xpath("//span[@id='lbl_nfsa']/text()").extract()
        address = response.xpath("//span[@id='lblPresentAddress']/text()").extract()
        mobile = response.xpath("//span[@id='lblmobile']/text()").extract()
        fps = response.xpath("//span[@id='lblfps']/text()").extract()
        mobile = response.xpath("//span[@id='lblmobile']/text()").extract()
        gas_agency = response.xpath("//span[@id='lblgasagency']/text()").extract()
        gas_agency_name = response.xpath("//span[@id='lblgasagencyname']/text()").extract()
        gas_consumer = response.xpath("//span[@id='lblgasconsumer']/text()").extract()
        item['Ration_Card_Number'] = card_no
        item['Card_Type'] = card_type
        item['Type_of_Food_Safety'] = nfsa
        item['Consumer_Name'] = app_name
        item['Address'] = address
        item['Mobile_Number'] = mobile
        item['Name_of_Fair_Price_Shopkeeper'] = fps
        item['Gas_Type'] = gas_agency
        item['Gas_Agency'] = gas_agency_name
        item['Consumer_Number'] = gas_consumer
        img = response.xpath("//img[@id='Image_M']")[0]
        try:
            filename = './html/%s/%s.jpg' % (dst, card_no)
            with open(filename, 'wb') as f:
                f.write(b64decode(img.attrib['src'].split(',')[1]))
        except Exception as e:
            self.log(e)
        item['Photo_Path'] = filename
        #print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', item)
        yield item

        try:
            dfs = pd.read_html(response.body, attrs={'id': 'grdFamilyDetail'})
            df = dfs[0]
            df.columns = ['S_No', 'Consumer_Name', 'Age', 'Father_Name', 'Relationship']
            df = df.astype({'S_No': int})
            df.insert(0, 'Ration_Card_Number', card_no)
            for i, r in df.iterrows():
                if dst == 'rural':
                    item = RationCardFamilyItem()
                else:
                    item = UrbanRationCardFamilyItem()
                for c in df.columns:
                    item[c] = r[c]
                yield item
        except Exception as e:
            print(e)

        try:
            dfs = pd.read_html(response.body, attrs={'id': 'GV_PosTransaction'})
            df = dfs[0]
            df.columns = ['Bill_Number', 'Bill_Date', 'Shop_Name', 'Type_of_Food', 'Quantity_of_Food']
            df.insert(0, 'Ration_Card_Number', card_no)
            for i, r in df.iterrows():
                if dst == 'rural':
                    item = RationCardTransactionItem()
                else:
                    item = UrbanRationCardTransactionItem()
                for c in df.columns:
                    item[c] = r[c]
                yield item
        except Exception as e:
            print(e)

    def parse_ration_card(self, response):
        print('************** Ration Card URL %s (meta=%r)' % (response.url, response.meta))
        gen = response.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").extract()[0]
        state = response.xpath("//input[@id='__VIEWSTATE']/@value").extract()[0]
        #print(gen, state)
        yield FormRequest('https://food.raj.nic.in/Search_RationCardDetails.aspx',
            formdata={'__VIEWSTATEGENERATOR': gen, '__VIEWSTATE': state},
            callback = self.parse_detail,
            dont_filter = True,
            #meta={'item': response.meta['item'], 'cookiejar': response.meta['cookiejar']})
            #meta={'item': response.meta['item']})
            meta={'item': response.meta['item'], 'cookiejar': response.meta['cookiejar']})

    def parse_fps(self, response):
        #print('FPS URL %s (meta=%r)' % (response.url, response.meta))
        page = response.meta.get('page', 0)
        fps_item = response.meta.get('item')
        for i, href in enumerate(response.xpath("//a[re:test(@id, 'grdFPS_lnkGo_\d+$')]")):
            item = RationCardItem()
            item['District_Code'] = fps_item['District_Code']
            item['Block_Code'] = fps_item['Block_Code']
            item['Panchayat_Code'] = fps_item['Panchayat_Code']
            item['Village_Code'] = fps_item['Village_Code']
            item['FPS_Code'] = fps_item['FPS_Code']
            for j, col in enumerate(href.xpath('../../td')):
                val = ''.join(col.xpath('.//text()').extract())
                item[RationCardItem.fields_to_export[j]] = val.strip()
            #print(item)
            #<input type="hidden" name="grdFPS$ctl02$hdnPLC_Code" id="grdFPS_hdnPLC_Code_0" value="0811900606091542">
            #<input type="hidden" name="grdFPS$ctl03$hdnUnique_RC_ID" id="grdFPS_hdnUnique_RC_ID_1" value="009154200002 ">
            card_no = response.xpath("//input[@id='grdFPS_hdnUnique_RC_ID_%d']/@value" % i).extract()[0].strip()
            #print(card_no)
            item['Ration_Card_Number'] = card_no
            key = '-'.join([item['District_Code'], item['Block_Code'], item['Panchayat_Code'], item['Village_Code'], item['FPS_Code'], item['Ration_Card_Number']])
            url = href.attrib['href']
            #print(i, url)
            filename = './html/rural/%s.jpg' % card_no
            detail = getattr(self, 'detail', 'no')
            if (detail == 'no') or os.path.exists(filename):
                #print('Skip...%s' % card_no)
                yield item
            else:
                yield item
                #print(url)
                m = re.match(".*?\((.*?)\,(.*?)\)", url)
                if m:
                    target = m.group(1).replace("'", "")
                    arg = m.group(2).replace("'", "")
                    #print(target, arg)
                    form = FormRequest.from_response(response,
                        formdata={'__EVENTTARGET': target, '__EVENTARGUMENT': arg},
                        callback = self.parse_ration_card,
                        dont_click = True,
                        dont_filter = True,
                        meta={'item': item, 'url': url, 'fork_from_cookiejar': response.meta['cookiejar'], 'cookiejar': key})
                    #print(form.body)
                    yield form
            #if i == 5:
            #    break

        href = response.xpath("//a[.='Next']")
        if len(href):
            url = href[0].attrib['href']
            m = re.match(".*?\((.*?)\,(.*?)\)", url)
            if m:
                target = m.group(1).replace("'", "")
                arg = m.group(2).replace("'", "")
                #print('********* NEXT FPS *********', target, arg)
                yield FormRequest.from_response(response,
                    formdata={'__EVENTTARGET': target, '__EVENTARGUMENT': arg},
                    callback = self.parse_fps,
                    dont_click = True,
                    meta={'item': item, 'page': page + 1, 'cookiejar': response.meta['cookiejar']})

    def parse_village(self, response):
        #print('Village URL %s (meta=%r)' % (response.url, response.meta))
        for i, href in enumerate(response.xpath("//a[re:test(@id, 'grdFPS_lnkGo_\d+$')]")):
            """
            <a id="grdFPS_lnkGo_1" href="javascript:__doPostBack('grdFPS$ctl03$lnkGo','')">1961-ग्राम सेवा सहकारी समिति ढसूक</a>
            <input type="hidden" name="grdFPS$ctl03$hdnPLC_Code" id="grdFPS_hdnPLC_Code_1" value="0811900606091542">
            <input type="hidden" name="grdFPS$ctl03$hdnFPS_Code" id="grdFPS_hdnFPS_Code_1" value="1961">
            <input type="hidden" name="grdFPS$ctl03$hdnFPS_OwnerName_LL" id="grdFPS_hdnFPS_OwnerName_LL_1" value="1961-ग्राम सेवा सहकारी समिति ढसूक">
            <input type="hidden" name="grdFPS$ctl03$hdnDistrictCode" id="grdFPS_hdnDistrictCode_1" value="119">
            """
            v_item = response.meta['item']
            f_code = href.xpath("../input[@id='grdFPS_hdnFPS_Code_%d']/@value" % i).extract()[0]
            item = FPSItem()
            item['District_Code'] = v_item['District_Code']
            item['Block_Code'] = v_item['Block_Code']
            item['Panchayat_Code'] = v_item['Panchayat_Code']
            item['Village_Code'] = v_item['Village_Code']
            item['FPS_Code'] = f_code
            for j, col in enumerate(href.xpath('../../td')):
                val = ''.join(col.xpath('.//text()').extract())
                item[FPSItem.fields_to_export[j]] = val.strip()
            yield item
            #if i > 0:
            #    continue
            #print('*************', f_code)
            key = '-'.join([v_item['District_Code'], v_item['Block_Code'], v_item['Panchayat_Code'], v_item['Village_Code'], f_code])
            url = href.attrib['href']
            #print(url)
            m = re.match(".*?\((.*?)\,(.*?)\)", url)
            if m:
                target = m.group(1).replace("'", "")
                arg = m.group(2).replace("'", "")
                yield FormRequest.from_response(response,
                    formdata={'__EVENTTARGET': target, '__EVENTARGUMENT': arg},
                    callback = self.parse_fps,
                    dont_click = True,
                    dont_filter = True,
                    meta={'item': item, 'fork_from_cookiejar': response.meta['cookiejar'], 'cookiejar': key})

    def parse_panchayat(self, response):
        #print('Panchayat URL %s (meta=%r)' % (response.url, response.meta))
        for i, href in enumerate(response.xpath("//a[re:test(@id, 'grdVillage_lnkGo_\d+$')]")):
            """
            <a id="grdVillage_lnkGo_0" href="javascript:__doPostBack('grdVillage$ctl02$lnkGo','')">माण्डियावडखुर्द</a>
            <input type="hidden" name="grdVillage$ctl02$hdnBlockCode" id="grdVillage_hdnBlockCode_0" value="0001">
            <input type="hidden" name="grdVillage$ctl02$hdnPanchayatCode" id="grdVillage_hdnPanchayatCode_0" value="0002">
            <input type="hidden" name="grdVillage$ctl02$hdnDistrictCode" id="grdVillage_hdnDistrictCode_0" value="119">
            <input type="hidden" name="grdVillage$ctl02$hdnPLC_Code" id="grdVillage_hdnPLC_Code_0" value="0811900606091542">
            <input type="hidden" name="grdVillage$ctl02$hdnVillageName" id="grdVillage_hdnVillageName_0" value="माण्डियावडखुर्द">
            """
            b_code = href.xpath("../input[@id='grdVillage_hdnBlockCode_%d']/@value" % i).extract()[0]
            p_code = href.xpath("../input[@id='grdVillage_hdnPanchayatCode_%d']/@value" % i).extract()[0]
            d_code = href.xpath("../input[@id='grdVillage_hdnDistrictCode_%d']/@value" % i).extract()[0]
            v_code = href.xpath("../input[@id='grdVillage_hdnPLC_Code_%d']/@value" % i).extract()[0]
            print(b_code, p_code, d_code, v_code)
            item = VillageItem()
            item['District_Code'] = d_code
            item['Block_Code'] = b_code
            item['Panchayat_Code'] = p_code
            item['Village_Code'] = v_code
            for j, col in enumerate(href.xpath('../../td')):
                val = ''.join(col.xpath('.//text()').extract())
                item[VillageItem.fields_to_export[j]] = val.strip()
            yield item
            #if i > 0:
            #    continue
            url = href.attrib['href']
            #print(url)
            m = re.match(".*?\((.*?)\,(.*?)\)", url)
            if m:
                target = m.group(1).replace("'", "")
                arg = m.group(2).replace("'", "")
                yield FormRequest.from_response(response,
                    formdata={'__EVENTTARGET': target, '__EVENTARGUMENT': arg},
                    callback = self.parse_village,
                    dont_click = True,
                    dont_filter = True,
                    meta={'item': item, 'fork_from_cookiejar': response.meta['cookiejar'], 'cookiejar': '-'.join([d_code, b_code, p_code, v_code])})

    def parse_block(self, response):
        #print('Block URL %s (meta=%r)' % (response.url, response.meta))
        for i, href in enumerate(response.xpath("//a[re:test(@id, 'grd_Panchayat_lnkGo_\d+$')]")):
            """
            <a id="grd_Panchayat_lnkGo_0" href="javascript:__doPostBack('grd_Panchayat$ctl02$lnkGo','')">ढसूक </a>
            <input type="hidden" name="grd_Panchayat$ctl02$hdnBlockCode" id="grd_Panchayat_hdnBlockCode_0" value="0001">
            <input type="hidden" name="grd_Panchayat$ctl02$hdnPanchayatCode" id="grd_Panchayat_hdnPanchayatCode_0" value="0002">
            <input type="hidden" name="grd_Panchayat$ctl02$hdnPanchayatName" id="grd_Panchayat_hdnPanchayatName_0" value="ढसूक ">
            <input type="hidden" name="grd_Panchayat$ctl02$hdnDistrictCode" id="grd_Panchayat_hdnDistrictCode_0" value="119">
            """
            d_code = href.xpath("../input[@id='grd_Panchayat_hdnDistrictCode_%d']/@value" % i).extract()[0]
            b_code = href.xpath("../input[@id='grd_Panchayat_hdnBlockCode_%d']/@value" % i).extract()[0]
            p_code = href.xpath("../input[@id='grd_Panchayat_hdnPanchayatCode_%d']/@value" % i).extract()[0]
            item = PanchayatItem()
            item['District_Code'] = d_code
            item['Block_Code'] = b_code
            item['Panchayat_Code'] = p_code
            for j, col in enumerate(href.xpath('../../td')):
                val = ''.join(col.xpath('.//text()').extract())
                item[PanchayatItem.fields_to_export[j]] = val.strip()
            yield item
            #if i > 0:
            #    continue
            url = href.attrib['href']
            #print(url)
            m = re.match(".*?\((.*?)\,(.*?)\)", url)
            if m:
                target = m.group(1).replace("'", "")
                arg = m.group(2).replace("'", "")
                yield FormRequest.from_response(response,
                    formdata={'__EVENTTARGET': target, '__EVENTARGUMENT': arg},
                    callback = self.parse_panchayat,
                    dont_click = True,
                    dont_filter = True,
                    meta={'item': item, 'fork_from_cookiejar': response.meta['cookiejar'], 'cookiejar': '-'.join([d_code, b_code, p_code])})

    def parse_rural(self, response):
        #print('Rural URL %s (meta=%r)' % (response.url, response.meta))
        #self.log('Rural URL %s (meta=%r)' % (response.url, response.meta))
        for i, href in enumerate(response.xpath("//a[re:test(@id, 'grd_Block_lnkGo_\d+$')]")):
            d_code = href.xpath("../input[@id='grd_Block_hdnDistrictCode_%d']/@value" % i).extract()[0]
            b_code = href.xpath("../input[@id='grd_Block_hdnBlockCode_%d']/@value" % i).extract()[0]
            item = BlockItem()
            item['District_Code'] = d_code
            item['Block_Code'] = b_code
            for j, col in enumerate(href.xpath('../../td')):
                val = ''.join(col.xpath('.//text()').extract())
                item[BlockItem.fields_to_export[j]] = val.strip()
            yield item
            #if i > 0:
            #    continue
            url = href.attrib['href']
            #print(url)
            m = re.match(".*?\((.*?)\,(.*?)\)", url)
            if m:
                target = m.group(1).replace("'", "")
                arg = m.group(2).replace("'", "")
                yield FormRequest.from_response(response,
                    formdata={'__EVENTTARGET': target, '__EVENTARGUMENT': arg},
                    callback = self.parse_block,
                    dont_click = True,
                    dont_filter = True,
                    meta={'item': item, 'fork_from_cookiejar': response.meta['cookiejar'], 'cookiejar': '-'.join([d_code, b_code])})


    def parse_urbanfps(self, response):
        #print('FPS URL %s (meta=%r)' % (response.url, response.meta))
        page = response.meta.get('page', 0)
        fps_item = response.meta.get('item')
        """
        <a id="grdFPS_lnkGo_0" href="javascript:__doPostBack('grdFPS$ctl02$lnkGo','')">************ </a>
        <input type="hidden" name="grdFPS$ctl02$hdnPLC_Code" id="grdFPS_hdnPLC_Code_0" value="0811900000012001">
        <input type="hidden" name="grdFPS$ctl02$hdnUnique_RC_ID" id="grdFPS_hdnUnique_RC_ID_0" value="101200101647 ">
        """
        for i, href in enumerate(response.xpath("//a[re:test(@id, 'grdFPS_lnkGo_\d+$')]")):
            item = UrbanRationCardItem()
            item['District_Code'] = fps_item['District_Code']
            item['Nagarpalika_Code'] = fps_item['Nagarpalika_Code']
            item['Ward_Code'] = fps_item['Ward_Code']
            item['FPS_Code'] = fps_item['FPS_Code']
            for j, col in enumerate(href.xpath('../../td')):
                val = ''.join(col.xpath('.//text()').extract())
                item[UrbanRationCardItem.fields_to_export[j]] = val.strip()
            #print(item)
            #<input type="hidden" name="grdFPS$ctl02$hdnPLC_Code" id="grdFPS_hdnPLC_Code_0" value="0811900606091542">
            #<input type="hidden" name="grdFPS$ctl03$hdnUnique_RC_ID" id="grdFPS_hdnUnique_RC_ID_1" value="009154200002 ">
            card_no = response.xpath("//input[@id='grdFPS_hdnUnique_RC_ID_%d']/@value" % i).extract()[0].strip()
            #print(card_no)
            item['Ration_Card_Number'] = card_no
            key = '-'.join([item['District_Code'], item['Nagarpalika_Code'], item['Ward_Code'], item['FPS_Code'], item['Ration_Card_Number']])
            url = href.attrib['href']
            #filename = './html/urban/%s.html.gz' % card_no
            filename = './html/urban/%s.jpg' % card_no
            detail = getattr(self, 'detail', 'no')
            if (detail == 'no') or os.path.exists(filename):
                #print('Skip...%s' % card_no)
                yield item
            else:
                yield item
                #print(url)
                m = re.match(".*?\((.*?)\,(.*?)\)", url)
                if m:
                    target = m.group(1).replace("'", "")
                    arg = m.group(2).replace("'", "")
                    #print(target, arg)
                    form = FormRequest.from_response(response,
                        formdata={'__EVENTTARGET': target, '__EVENTARGUMENT': arg},
                        callback = self.parse_ration_card,
                        dont_click = True,
                        dont_filter = True,
                        meta={'item': item, 'url': url, 'fork_from_cookiejar': response.meta['cookiejar'], 'cookiejar': key})
                    #print(form.body)
                    yield form
            #if i == 5:
            #    break

        href = response.xpath("//a[.='Next']")
        if len(href):
            url = href[0].attrib['href']
            m = re.match(".*?\((.*?)\,(.*?)\)", url)
            if m:
                target = m.group(1).replace("'", "")
                arg = m.group(2).replace("'", "")
                #print('********* NEXT FPS *********', target, arg)
                yield FormRequest.from_response(response,
                    formdata={'__EVENTTARGET': target, '__EVENTARGUMENT': arg},
                    callback = self.parse_urbanfps,
                    dont_click = True,
                    meta={'item': item, 'page': page + 1, 'cookiejar': response.meta['cookiejar']})

    def parse_ward(self, response):
        #print('Village URL %s (meta=%r)' % (response.url, response.meta))
        """
        <a id="grdFPS_lnkGo_0" href="javascript:__doPostBack('grdFPS$ctl02$lnkGo','')">अजमेर सह उप होल सेल भण्&zwj;डार श्री रामचरण</a>
        <input type="hidden" name="grdFPS$ctl02$hdnNagarpalikaId" id="grdFPS_hdnNagarpalikaId_0" value="012">
        <input type="hidden" name="grdFPS$ctl02$hdnPLC_Code" id="grdFPS_hdnPLC_Code_0" value="0811900000012001">
        <input type="hidden" name="grdFPS$ctl02$hdnFPS_Code" id="grdFPS_hdnFPS_Code_0" value="17252">
        <input type="hidden" name="grdFPS$ctl02$hdnFPS_OwnerName_LL" id="grdFPS_hdnFPS_OwnerName_LL_0" value="अजमेर सह उप होल सेल भण्&zwj;डार श्री रामचरण">
        <input type="hidden" name="grdFPS$ctl02$hdnDistrictCode" id="grdFPS_hdnDistrictCode_0" value="119">
        """
        ward_item = response.meta.get('item')
        for i, href in enumerate(response.xpath("//a[re:test(@id, 'grdFPS_lnkGo_\d+$')]")):
            f_code = href.xpath("../input[@id='grdFPS_hdnFPS_Code_%d']/@value" % i).extract()[0]
            item = UrbanFPSItem()
            item['District_Code'] = ward_item['District_Code']
            item['Nagarpalika_Code'] = ward_item['Nagarpalika_Code']
            item['Ward_Code'] = ward_item['Ward_Code']
            item['FPS_Code'] = f_code
            for j, col in enumerate(href.xpath('../../td')):
                val = ''.join(col.xpath('.//text()').extract())
                item[UrbanFPSItem.fields_to_export[j]] = val.strip()
            yield item
            #if i > 0:
            #    continue
            #print('*************', f_code)
            key = '-'.join([item['District_Code'], item['Nagarpalika_Code'], item['Ward_Code'], item['FPS_Code']])
            url = href.attrib['href']
            #print(url)
            m = re.match(".*?\((.*?)\,(.*?)\)", url)
            if m:
                target = m.group(1).replace("'", "")
                arg = m.group(2).replace("'", "")
                yield FormRequest.from_response(response,
                    formdata={'__EVENTTARGET': target, '__EVENTARGUMENT': arg},
                    callback = self.parse_urbanfps,
                    dont_click = True,
                    dont_filter = True,
                    meta={'item': item, 'fork_from_cookiejar': response.meta['cookiejar'], 'cookiejar': key})

    def parse_nagarpalika(self, response):
        #print('Block URL %s (meta=%r)' % (response.url, response.meta))
        """
        <a id="grd_Ward_lnkGo_0" href="javascript:__doPostBack('grd_Ward$ctl02$lnkGo','')">वार्ड 1</a>
        <input type="hidden" name="grd_Ward$ctl02$hdnNagarpalikaId" id="grd_Ward_hdnNagarpalikaId_0" value="012">
        <input type="hidden" name="grd_Ward$ctl02$hdnPLC_Code" id="grd_Ward_hdnPLC_Code_0" value="0811900000012001">
        <input type="hidden" name="grd_Ward$ctl02$hdnWard_No" id="grd_Ward_hdnWard_No_0" value="वार्ड 1">
        <input type="hidden" name="grd_Ward$ctl02$hdnDistrictCode" id="grd_Ward_hdnDistrictCode_0" value="119">
        """
        for i, href in enumerate(response.xpath("//a[re:test(@id, 'grd_Ward_lnkGo_\d+$')]")):
            d_code = href.xpath("../input[@id='grd_Ward_hdnDistrictCode_%d']/@value" % i).extract()[0]
            n_code = href.xpath("../input[@id='grd_Ward_hdnNagarpalikaId_%d']/@value" % i).extract()[0]
            w_code = href.xpath("../input[@id='grd_Ward_hdnPLC_Code_%d']/@value" % i).extract()[0]
            item = WardItem()
            item['District_Code'] = d_code
            item['Nagarpalika_Code'] = n_code
            item['Ward_Code'] = w_code
            for j, col in enumerate(href.xpath('../../td')):
                val = ''.join(col.xpath('.//text()').extract())
                item[WardItem.fields_to_export[j]] = val.strip()
            yield item
            #if i > 0:
            #    continue
            url = href.attrib['href']
            #print(url)
            m = re.match(".*?\((.*?)\,(.*?)\)", url)
            if m:
                target = m.group(1).replace("'", "")
                arg = m.group(2).replace("'", "")
                yield FormRequest.from_response(response,
                    formdata={'__EVENTTARGET': target, '__EVENTARGUMENT': arg},
                    callback = self.parse_ward,
                    dont_click = True,
                    dont_filter = True,
                    meta={'item': item, 'fork_from_cookiejar': response.meta['cookiejar'], 'cookiejar': '-'.join([d_code, n_code, w_code])})

    def parse_urban(self, response):
        #print('Rural URL %s (meta=%r)' % (response.url, response.meta))
        #self.log('Rural URL %s (meta=%r)' % (response.url, response.meta))
        """
        <a id="grd_Nagarpalika_lnkGo_0" href="javascript:__doPostBack('grd_Nagarpalika$ctl02$lnkGo','')">अजमेर</a>
        <input type="hidden" name="grd_Nagarpalika$ctl02$hdnNagarPalikaCode" id="grd_Nagarpalika_hdnNagarPalikaCode_0" value="012">
        <input type="hidden" name="grd_Nagarpalika$ctl02$hdnNagarPalikaName" id="grd_Nagarpalika_hdnNagarPalikaName_0" value="अजमेर">
        <input type="hidden" name="grd_Nagarpalika$ctl02$hdnDistrictCode" id="grd_Nagarpalika_hdnDistrictCode_0" value="119">
        """
        for i, href in enumerate(response.xpath("//a[re:test(@id, 'grd_Nagarpalika_lnkGo_\d+$')]")):
            d_code = href.xpath("../input[@id='grd_Nagarpalika_hdnDistrictCode_%d']/@value" % i).extract()[0]
            n_code = href.xpath("../input[@id='grd_Nagarpalika_hdnNagarPalikaCode_%d']/@value" % i).extract()[0]
            item = NagarpalikaItem()
            item['District_Code'] = d_code
            item['Nagarpalika_Code'] = n_code
            for j, col in enumerate(href.xpath('../../td')):
                val = ''.join(col.xpath('.//text()').extract())
                item[NagarpalikaItem.fields_to_export[j]] = val.strip()
            yield item
            #if i > 0:
            #    continue
            url = href.attrib['href']
            print(i, url)
            m = re.match(".*?\((.*?)\,(.*?)\)", url)
            if m:
                target = m.group(1).replace("'", "")
                arg = m.group(2).replace("'", "")
                yield FormRequest.from_response(response,
                    formdata={'__EVENTTARGET': target, '__EVENTARGUMENT': arg},
                    callback = self.parse_nagarpalika,
                    dont_click = True,
                    dont_filter = True,
                    meta={'item': item, 'fork_from_cookiejar': response.meta['cookiejar'], 'cookiejar': '-'.join([d_code, n_code])})