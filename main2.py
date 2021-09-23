import pandas as pd
from geoip import geolite2
from urllib.parse import urlparse


def find_info_with_request(my_df):
    request_list = df['%r'].tolist()

    method_list = []

    url_scheme_list = [] #Протокол
    url_netloc_list = [] #Доменное имя
    url_path_list = [] #Путь
    url_params_list = [] #Параметры последнего элемента пути
    url_query_list = [] #Компонент запроса
    url_fragment_list = [] #Идентификатор фрагмента

    http_list = []

    for i in request_list:
        try:
            method, url, http = i.split()
            method_list.append(method)
            url_line = urlparse(url)

            if url_line.scheme == '':
                url_scheme_list.append('no url scheme')
            else:
                url_scheme_list.append(url_line.scheme)

            if url_line.netloc == '':
                url_netloc_list.append('no url netloc')
            else:
                url_netloc_list.append(url_line.netloc)

            if url_line.path == '':
                url_path_list.append('no url path')
            else:
                url_path_list.append(url_line.path)

            if url_line.params == '':
                url_params_list.append('no url params')
            else:
                url_params_list.append(url_line.params)

            if url_line.query == '':
                url_query_list.append('no url query')
            else:
                url_query_list.append(url_line.query)

            if url_line.fragment == '':
                url_fragment_list.append('no url fragment')
            else:
                url_fragment_list.append(url_line.fragment)

            http_list.append(http)
        except:
            method_list.append('error in request')
            url_scheme_list.append('error in request')
            url_netloc_list.append('error in request')
            url_path_list.append('error in request')
            url_params_list.append('error in request')
            url_query_list.append('error in request')
            url_fragment_list.append('error in request')
            http_list.append('error in request')

    my_df['method'] = method_list
    my_df['url_sheme'] = url_scheme_list
    my_df['url_netloc'] = url_netloc_list
    my_df['url_path'] = url_path_list
    my_df['url_params'] = url_params_list
    my_df['url_querty'] = url_query_list
    my_df['url_fragment'] = url_fragment_list
    my_df['http'] = http_list
    print('the function has finished working')
    return my_df


def find_info_with_ip(my_df):
    ip_list = df['%h'].tolist()

    for i in ip_list:

        apend_list = []

        try:
            m = geolite2.lookup(i)
            contry = m.country
        except:
            contry = "can't find country"

        try:
            m = geolite2.lookup(i)
            continent = m.continent
        except:
            continent = "can't find continent"

        try:
            m = geolite2.lookup(i)
            subdivisions = m.subdivisions
        except:
            subdivisions = "can't find subdivisions"

        try:
            m = geolite2.lookup(i)
            timezone = m.timezone
        except:
            timezone = "can't find timezone"

        apend_list = [i, contry, continent, subdivisions, timezone]
        apend_list = pd.Series(apend_list, index=col_names)
        my_df = my_df.append(apend_list, ignore_index=True)


    print('the function has finished working')
    return my_df

if __name__ == '__main__':
    col_names = ['ip', 'country', 'continent', 'subdivisions', 'timezone']
    my_df = pd.DataFrame(columns=col_names)

    df = pd.read_csv('parse_accessLog.csv', sep=';')

    my_df = find_info_with_ip(my_df)
    my_df = find_info_with_request(my_df)
    my_df.to_csv('DictForLearn.csv', sep=';')