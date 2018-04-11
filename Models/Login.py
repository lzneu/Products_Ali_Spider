#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 此项目主要参考链接【http://cuiqingcai.com/1076.html，感谢作者的分享

__author__ = 'JustFantasy'

import urllib.request, urllib.parse, urllib.error
import http.cookiejar
import re
import socket
# 模拟登录淘宝类
# 登录淘宝流程
# 1、请求地址https://login.taobao.com/member/login.jhtml获取到token
# 2、请求地址https://passport.alibaba.com/mini_apply_st.js?site=0&token=1L1nkdyfEDIA44Hw1FSDcnA&callback=callback 通过token换取st
# 3、请求地址https://login.taobao.com/member/vst.htm?st={st}实现登录
class Taobao:

    # 初始化方法
    def __init__(self):
        # 登录的URL，获取token
        self.request_url = 'https://login.taobao.com/member/login.jhtml'
        # 通过st实现登录的URL
        self.st_url = 'https://login.taobao.com/member/vst.htm?st={st}'
        # 用户中心地址
        self.user_url = 'https://rate.taobao.com/feedRateList.htm?auctionNumId=45670751318&userNumId=498026345&currentPageNum=1&pageSize=20&rateType=&orderType=sort_weight&attribute=&sku=&hasSku=false&folded=0&ua=098%23E1hvU9vEvbQvUpCkvvvvvjiPP2dWAj3PRLS9sjljPmPWAj1ERF5w6jnhPsdZQj3nRsyCvvBvpvvv2QhvC26wT9eEvpvVpyUUCCKOuphvmhCvCj5fwF%2BzKphv8hCvvvvvvhCvphvw%2FpvvpMXvpCQmvvChNhCvjvUvvhBZphvwv9vvBHpEvpCWBj4tv8RrJoBYWUcBn86DN5vra4mAdch%2B4Z7xfBkKNZl%2BmPLheCiQBeQ4S4ZAhjvnPBcB%2BbJcwyOG28L%2BWLyDBm%2BpFO7t%2BeCBaZ%2FhephCvvXvppvvvvm5vpvhphvhHUwCvvBvppvv&_ksTS=1506323758157_2306&callback=jsonp_tbcrate_reviews_list'
        # 代理IP地址，防止自己的IP被封禁
        self.proxy_ip = 'http://120.193.146.97:843'
        # 登录POST数据时发送的头部信息
        self.request_headers = {
            'Host':'login.taobao.com',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Referer' : 'https://login.taobao.com/member/login.jhtml',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection' : 'Keep-Alive'
        }
        # 用户名
        self.username = '13840512781'
        # ua字符串，经过淘宝ua算法计算得出，包含了时间戳,浏览器,屏幕分辨率,随机数,鼠标移动,鼠标点击,其实还有键盘输入记录,鼠标移动的记录、点击的记录等等的信息
        self.ua = '098#E1hvVpv4vewvn9CkvvvvvjiPP2dWAjibPssW1jthnLcWQjtP4FAX1j38R7kBQm9O4FunFcDRRFzp6j6X4FcZyctP4FSv3fwCvCoV3IeEtjPwFWofMUMM2R4jtO27tghCvCuaNEEfxaMwznQDhHIu6y488U52s5EqmVIEobwCvCoV3geElt5wFWofMUMM2R4jtO27tsyCvvpvvhCv9phvVilGmlIczYswzUP37kdoCIIEoW7Ww5+U49DURphvCvvvphmrvpvEvvmMSMGvvUvLdphvmpvvu4DdvvmvvTwCvvpvvhHhRphvCvvvphvPvpvh6GH03phCvvOv9hCvvvvEvpCW9o1i4Bzh5E+7RAYVyOvO5fVQWl4vAC9aRfU6pwethb8rejOdd8Q7WiTwahjy+2Kzr2E9ZRAn+beAhjE2TWeARdItb9TxfX9OdigDNkhCv8KUVUeJv9qGFPSCiIyVmJ/Vt+FY5v5GTO4e1J4bApNr9RuP/YpVmJ/Vt+FFkQgjtnSqk/LX/GAt0/NESUso6buZSguY3aPRSU/Myfk7swAQ6fARTIsohJT6+N7SAawRttJKzRAUvQsrFSAi0tNcvSAU/UK+5+MnAJATFqSYSGAYFGTtMI5U2KeVTISeAP6EtwmTFqSYv9qGFPSCiIyBhNMBMEze3P+Ei+c5ku4tvpvIvvCvpvvvvvvvvhPYvvmCQvvvBGwvvvUwvvCj1Qvvv99vvhREvvvmmUyCvv4CvhE2lnoivpvUvvCCjYqAW9mjvpvhvUCvp86CvvyvvRPFnpvvvn/rvpvEvvmPFtOvvvCsdphvmpmvZxC+vvmvUQwCvvNwoli4z12KrQhvCIkUkOeF/bwCvv4UkOeEllwtvpvhvvCvpbwCvCoV3geEtjMm5aKKTgO22rKSTXz99Q=='
        # 密码，在这里不能输入真实密码，淘宝对此密码进行了加密处理，256位，此处为加密后的密码
        self.password2 = '92dd8e73bbe14f57e828f2d8ffadfa78f186c43ba61b4a027209702ebb97436f4d8492695bbf79583bd3f099d085dc80ac9e369a1f4faf37528846926b5e4abe21ae6589f62c4878aa6a60769db8fd985d751fbd209f620b72d2cfa4ed6a90abe4ecb286d86afccf0d9a87099c80f3bd72b3fe4ed751bd3918f69c8794f00fef'
        # self.post = {
        #     'ua': self.ua,
        #     'TPL_checkcode': '',
        #     'CtrlVersion': '1,0,0,7',
        #     'TPL_password': '',
        #     'TPL_redirect_url': 'https://www.taobao.com/',
        #     'TPL_username': self.username,
        #     'loginsite': '0',
        #     'newlogin': '0',
        #     'from': 'tb',
        #     'fc': 'default',
        #     'style': 'default',
        #     'css_style': '',
        #     'tid': '',
        #     'support': '000001',
        #     'loginType': '4',
        #     'minititle': '',
        #     'minipara': '',
        #     'umto': 'NaN',
        #     'pstrong': '3',
        #     'llnick': '',
        #     'sign': '',
        #     'need_sign': '',
        #     'isIgnore': '',
        #     'full_redirect': '',
        #     'popid': '',
        #     'callback': '',
        #     'guf': '',
        #     'not_duplite_str': '',
        #     'need_user_id': '',
        #     'poy': '',
        #     'gvfdcname': '10',
        #     'gvfdcre': '',
        #     'from_encoding ': '',
        #     'sub': '',
        #     'TPL_password_2': self.password2,
        #     'loginASR': '1',
        #     'loginASRSuc': '1',
        #     'allp': '',
        #     'oslanguage': 'zh-CN',
        #     'sr': '1366*768',
        #     'osVer': 'windows|6.1',
        #     'naviVer': 'firefox|35'
        # }
        self.post = {
            'TPL_username' : self.username,
            'TPL_password':'',
            'ncoSig':'05lXxnxdScFJ2253v5luDa1-v70AGgjRmQ8jI1oK9lIn4J-Fa1IwpzXLqT01BV55jBaSrwVQXd4hDbF2_dAqpovVMQzHpw9bgZ-UT2LoL8IDpkm4WKt6wQdptFzWmNbi8BjDnThNyI3RPn-ksf6M5hQ-WgD52Lrdpcb5yTlaofjErX28utv7KUinxDvHbTSBvfKiTVgvxHlXUxjSSErkw0DKmQQM6Uj9h2bGCxqVpDOoyxSQtyhvBba92XsjUQ9b-GGv93LhdnQJr--XD7PW7b0IYlLL2IFYnLoRYuxdpceUk9yNaOj0SFifmcWtxxYxyAygjLh6-ncuhSo6Gyx2wiluvvGTG_p2mOJccLm5mPnFOVLUfG1e8XZnvybJzTD7bGdbf_63wXGSsrMa-iijIw9E22MOIVxAB584l4YQY6vNDTMaivDPrwhcxDb7NJxcDU137CR4MzQICFtzwgQ5pRSNK6Pexo2aZyLKLlSFWq3AKHvWE-pcAsmJ_LABmZoVX6oha7sfkXmYZCw-Oumg2DYvTQ-4AuErve9QQCfb_ek-ezTn2RATe3XLgm7e5T1TXIDxQmD61KpZRfUJh11HuspgJsTDnysdziz5EgkNDL8Iqz1xe0mrjc-exIsug2SttjPRkVLWbPjPgc_kP0-Qd1BAjAwJ2wH0PUKNs9BJr20WAfUT7nKUKXT9WUedBwY5XmRoChE5AadmcHEVE38P0a4A',
            'ncoSessionid':'01e6slx8dFdpbVo4wZeLTVwz6r2ED2ncrrGZWr4raWvuDI9JkAX2IKpycEtR-jCLOetBOrjLnHwlcM_YesxGq4B7p-7c6T9dCyHuXCRCVZiKGW17Q8CnVzzghdW-jDoBHgRU0xv1sxK0Gl37gleM614ftiJHFWsbqxmp1OTkGVrCCTNwOe3i8mJ3LxtguLqxuM-UtNTrfTFD90syaixOXGUWUa9Qh-ensLQ_L_S24uc1FhKaqJX1urO40rZEvCZZzjdJFKzq7JXE6pfiF2hq_g7nx1O5HHj2rmPbQvEqneL4IjTMKrxCMdKuuE8KHROOswIMZH0nRkpPTIY3rXHhdqtt_aJROU8KYsK7xB9q2ns24WvfkQqYKd0M5Ek4dD-qLafW5ayizBLA8chxrXW0vHBw',
            'ncoToken': 'd0daf13c15013c302eaf41d50269c6e665d09eb1',
            'slideCodeShow' : False,
            'useMobile' : False,
            'lang' : 'zh_CN',
            'loginsite': '0',
            'newlogin': '0',
            'TPL_redirect_url' : 'https://www.taobao.com/',
            'from': 'tbTop',
            'fc': 'default',
            'style': 'default',
            'css_style': '',
            'keyLogin': False,
            'qrLogin': True,
            'newMini': False,
            'newMini2': False,
            'tid' : '',
            'loginType': '3',
            'minititle':'',
            'minipara':'',
            'pstrong':'',
            'sign':'',
            'need_sign':'',
            'isIgnore':'',
            'full_redirect':'',
            'sub_jump':'',
            'popid':'',
            'callback':'',
            'guf':'',
            'not_duplite_str':'',
            'need_user_id':'',
            'poy':'',
            'gvfdcname': '10',
            'gvfdcre': '68747470733A2F2F6C6F67696E2E74616F62616F2E636F6D2F6D656D6265722F6C6F676F75742E6A68746D6C3F73706D3D613231626F2E35303836322E3735343839343433372E362E363063323363643935626B556B3926663D746F70266F75743D7472756526726564697265637455524C3D68747470732533412532462532467777772E74616F62616F2E636F6D253246',
            'from_encoding':'',
            'sub':'',
            'TPL_password_2': self.password2,
            'loginASR': '1',
            'loginASRSuc': '1',
            'allp': '',
            'oslanguage':'zh-CN',
            'sr': '1920*1080',
            'osVer':'',
            'naviVer': 'firefox|55',
            'osACN':'Mozilla',
            'osAV': '5.0+(Windows)',
            'osPF': 'Win32',
            'miserHardInfo': '',
            'appkey': '',
            'nickLoginLink': '',
            'mobileLoginLink':'https://login.taobao.com/member/login.jhtml?spm=a21bo.50862.754894437.1.328a42cf8wfZ9D&f=top&redirectURL=https://www.taobao.com/&useMobile=true',
            'showAssistantLink':'',
            'ua':'098#E1hv49vqCe6vn9CkvvvvvjiPP2dptjinPL5ysj3mfLAB3o6wP0dhljr8P0dWQjyw4VMp1mG4P2qOtm9Jf2dOlmGNn7AE12hCvntCpOQvj2vzxACv9OhQWmCvUhmC9LvQUhv9pUjxWbytpsnL9OhQWmCZpAyvjvv2pHEvLvvQvvavL6Cov2pv36CnphgvWvmHphDvBQvIvvEvBZChvvQvvyC2phOvVvmCphnCTpvhvUCvpyC2vvvvvhCvphvvvvvvphCvpvvvvvCvphCvvvvvvbYvph2MMQvvS6CvpPMMMM/MphCvvmQvm6CbphOv8vmmphDvB9v+vUEvohCUvmvvChCUph9vUvmhphavopvwvvBvohCUvmvvChCUph9vUvmhphavopvwvvorvpvBohsQCH9vpVXxRglYe8GKjsurvpvBohAgCH9vpVXh8IlYe8GKjsuCvpvZVPwEMvH4zYMNv4bwAbzoOaEbvkKrvpvBohKiCnWvpVLykIlYe8GKjsurvpvBohK1CnWvpVLZKIlYe8GKjsurvpvBohKlCHpvpVLHuglYe8GKjsurvpvBohSHCnpvpVBYhglYe8GKjsIjvpvXonMwzHiqaji4R+NuKGlsylnd4WJbAKEswQwCvCDUzYsw75DaJDIT1/uqscRLZ0rI1gS8g5nsCQhvVZFNzn14JB3T7FdjTdSnwtnL40FjkGdkwzWjvpvXonMwzHizWzi4R+NuKGlsylnd4WJbAKEswQwCvCDUzYsw754wJDIT1/uqscRLZ0rI1gS8g5nsRphvChCvvvmzvpvZ3g44eiiVzOzHe9GnqXM53KoC/wKzvpvVkOk4eiIk9phvVyFM8aQ/7rMNz0F1z8otOIWFGyykdwqkJAPARphvChCvvvmrvpvEphRqvnOvphhxdphvmZC2jp24vhCvMUwCvvBvppvviQhvChCvCCpPvpvhPBsumfyCvm3vpvvvvvCvphCvhW+vvhnbphvwv9vvBj1vpCQmvvChxhCvHvvvvhPduphvmhCvCj59G1UTkphvCyn2mvo4VohCvP0EliI6gELYFNdvAw5yk/TjtGyR//JHTUJ51vyjiGd+9JKR2W5yk/TjtGyhvSABtadq5Sg2/iMu5rARtrN9DP0n/rMWsqSTdETGFKmMKI/qMNTEhwFG5J4hTUNUMJJ8dETGFKvmMUFtkdRwApf59RmRiYPqmJubt+Fu3pNEtO2y3KAJApf59R4LMaWhvSABtadTk9NcTaKg0KfUsGuQ3dKxSISR6dVHSOT/yn2USIqu0bdXMrRYz/8zgrSvvbcCti4SQvGRrwjqFKs82PM+3NKJTiqSqWLtgXcYFp0MKI/T/TAJsGsRTqKRKM6BhNMBMXse3P+Ei+cekTAJsGsRmphvLhPA/9mFjjnhJxcXSfpAOHCqVUcn+3C1ocIUDaVTRogREcqWaXTAVA9anIktuuOEL7ERD76Od56ZVztrs8TK4hH+mPLhjCDgx2XXiXhCvpvVphhvvvvvRphvChCvvvmzvpvVkOk4eI9+dphvmZCmZQ28vhCvq46CvvDvpqgvcpCvp7RrvpvEphnMvnQvphH1CQhvCY/szn14OWKzvpvVkOe4eIHvRphvChCvvvmCvpv4oPwXMWn4zYMNyRNwduIT6DSkoydBA7ST6eVzvpvZ3gJ4eiMqzOzHe9GnqXM53KoC/wKzvpvZ3g44eiMSzOzHe9dq/gF/yNKN/w+jvpvXonMwzHi0Wji4R+NuKGlsylnd4WJbAKEswsyCvvBvpvvvRphvChCvvvvjvpvXonMwzHiznji4R+NuKGlsylnd4WJbAKEswQwCvCDUzYsw759yJDIT1/uqscRLZ0rI1gS8g5nsCQhvVZFNzn14JmtT7FdjTdSnwtnL40FjkGdkwzWjvpvXonMwzHitQzi4R+NuKGlsylnd4WJbAKEswQwCvCDUzYsw75dzJDIT1/uqscRLZ0rI1gS8g5nsdphvhZ3bQpLZvhCyCeknNXkSb3GTdphvhZ3bSpLZvhCy2V8nNXkSb3GTdphvhZ3bKpLZvhCybh8nNXkSb3GTdphvhZ3bipLLvhCyYEunNXkSb3GTRphvChCvvvmrvpvBohKiCHpvpVZrpglYe8GKjsurvpvBohKiCnpvpVZz7OlYe8GKjsurvpvBohSHCHZvpVcnIglYe8GKjsurvpvBohSaCnZvpVcXrglYe8GKjsurvpvBohAwCH9vpV7G6IlYe8GKjsuCvpv4oPNOMh34zYMN7ObwibDA9/i2m7ursKEqUMU=',
            'um_token': 'HV01PAAZ0b87180bafa09eac59cb3d3b001644dd'
        }


        # 设置超时
        socket.setdefaulttimeout(15)
        # 将POST的数据进行编码转换
        self.post_data = urllib.parse.urlencode(self.post).encode(encoding='GBK')
        # 设置代理
        self.proxy = urllib.request.ProxyHandler({'http': self.proxy_ip})
        # 设置cookie
        self.cookie = http.cookiejar.LWPCookieJar()
        # 设置cookie处理器
        self.cookieHandler = urllib.request.HTTPCookieProcessor(self.cookie)
        # 设置登录时用到的opener，它的open方法相当于urllib2.urlopen
        self.opener = urllib.request.build_opener(self.cookieHandler, urllib.request.HTTPHandler)
        # 赋值J_HToken
        self.J_HToken = ''
        # 登录成功时，需要的Cookie
        self.newCookie = http.cookiejar.CookieJar()
        # 登陆成功时，需要的一个新的opener
        self.newOpener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.newCookie))

    # 利用st码进行登录
    # 这一步我是参考的崔庆才的个人博客的教程，因为抓包的时候并没有抓取到这个url
    # 但是如果不走这一步，登录又无法成功
    # 区别是并不需要传递user_name字段，只需要st就可以了
    def login_by_st(self, st):
        st_url = self.st_url.format(st=st)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Host': 'login.taobao.com',
            'Connection': 'Keep-Alive'
        }
        request = urllib.request.Request(st_url, headers=headers)
        response = self.newOpener.open(request)
        content = response.read().decode('gbk')

        #检测结果，看是否登录成功
        pattern = re.compile('top.location.href = "(.*?)"', re.S)
        match = re.search(pattern, content)
        print(match)
        if match:
            print(u'登录网址成功')
            return True
        else:
            print(u'登录失败')
            return False


    # 程序运行主干
    def main(self):
        try:
            # 请求登录地址， 此时返回的页面中有两个js的引入
            # 位置是页面的前两个JS的引入，其中都带有token参数
            request = urllib.request.Request(self.request_url, self.post_data, self.request_headers)
            response = self.opener.open(request)
            content = response.read().decode('gbk')
            # 抓取页面中的两个获取st的js
            pattern = re.compile('<script src=\"(.*)\"><\/script>')
            match = pattern.findall(content)

            # [
            # 'https://passport.alibaba.com/mini_apply_st.js?site=0&token=1f2f3ePAx5b-G8YbNIlDCFQ&callback=callback',
            # 'https://passport.alipay.com/mini_apply_st.js?site=0&token=1tbpdXJo6W1E4bgPCfOEiGw&callback=callback',
            # 'https://g.alicdn.com/kissy/k/1.4.2/seed-min.js',
            # 'https://g.alicdn.com/vip/login/0.5.43/js/login/miser-reg.js?t=20160617'
            # ]
            # 其中第一个是我们需要请求的JS，它会返回我们需要的st
            #print(match)

            # 如果匹配到了则去获取st
            if match:
                # 此时可以看到有两个st， 一个alibaba的，一个alipay的，我们用alibaba的去实现登录
                request = urllib.request.Request(match[0])
                response = urllib.request.urlopen(request)
                content = response.read().decode('gbk')

                # {"code":200,"data":{"st":"1lmuSWeWh1zGQn-t7cfAwvw"} 这段JS正常的话会包含这一段，我们需要的就是st
                #print(content)

                # 正则匹配st
                pattern = re.compile('{"st":"(.*?)"}')
                match = pattern.findall(content)

                # 利用st进行登录
                if match:
                    self.login_by_st(match[0])
                else:
                    print(u'无法获取到st，请检查')
                    return self.opener

                # 请求用户中心，查看打印出来的内容，可以看到用户中心的相关信息
                # response = self.newOpener.open(url)
                # page = response.read().decode('gbk')
                # return page
                return self.newOpener
        except urllib.error.HTTPError as e:
            print(u'请求失败，错误信息：', e.msg)
