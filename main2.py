import pandas as pd
from geoip import geolite2
from urllib.parse import urlparse
import re
from dateutil.parser import parse as dateparser
from user_agents import parse


def copy_size_return_object(my_df, df):
    size_return_object_list = df['%b'].tolist()
    new_size_return_object_list = []

    for line in size_return_object_list:
        try:
            new_size_return_object_list.append(int(line))
        except:
            new_size_return_object_list.append(0)

    my_df['size_object'] = new_size_return_object_list
    print('the function "copy_size_return_object" has finished working')
    return my_df


def status_code_processing(my_df, df):
    status_code_list = df['%>s'].tolist()

    processing_status_code_list = []

    for line in status_code_list:
        try:
            cod = str(line)
            processing_status_code_list.append('status_code_' + cod[0])
        except:
            processing_status_code_list.append('no information')

    my_df['status_code'] = processing_status_code_list

    print('the function "status_code_processing" has finished working')
    return my_df


def find_info_with_Useragent(my_df, df):
    useragent_list = df['%{Useragent}i'].tolist()
    req_request = re.compile(r'([a-zA-z]+).')

    os_list = []
    browser_list = []
    device_list = []
    exit_system_list = []
    result = None


    for line in useragent_list:
        user_agent = parse(line)

        try:
            os_list.append(user_agent.os.family)
        except:
            os_list.append('no information')

        try:
            browser_list.append(user_agent.browser.family)
        except:
            browser_list.append('no information')

        try:
            device_list.append(user_agent.device.family)
        except:
            device_list.append('no information')

        try:
            result = req_request.match(line)
            exit_system_list.append(result.group(1))
        except:
            exit_system_list.append('no information')

    my_df['exit_system'] = exit_system_list
    my_df['os'] = os_list
    my_df['browser'] = browser_list
    my_df['device'] = device_list

    print('the function "find_info_with_Useragent" has finished working')
    return my_df


def separation_date_time(my_df, df):
    datetime_list = df['%t'].tolist()
    req_requset = re.compile(r'.([0-9]+.[a-zA-Z]+.[0-9]+).([0-9]+:[0-9]+:[0-9]+).([0-9]+).(.[0-9]+)')

    date_and_time = ''
    result = None
    date_list = []
    time_list = []
    timezone_list = []

    for line in datetime_list:
        result = req_requset.match(line)
        date_and_time = result.group(1) + ' ' + result.group(2)

        timezone_list.append(result.group(4))

        dt = dateparser(date_and_time)
        date_list.append(dt.date())
        time_list.append(dt.time())


        date_and_time = ''
        result = None


    my_df['date'] = date_list
    my_df['time'] = time_list
    my_df['time_zone'] = timezone_list

    print('the function "separation_date_time" has finished working')
    return my_df


def find_info_with_request(my_df, df):
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
    print('the function "find_info_with_request" has finished working')
    return my_df


def find_info_with_ip(my_df, df):
    ip_list = df['%h'].tolist()

    for i in ip_list:

        apend_list = []
        m = geolite2.lookup(i)


        try:
            contry = m.country
        except:
            contry = "can't find country"

        try:
            continent = m.continent
        except:
            continent = "can't find continent"

        try:
            subdivisions = m.subdivisions
        except:
            subdivisions = "can't find subdivisions"

        try:
            timezone = m.timezone
        except:
            timezone = "can't find timezone"

        apend_list = [i, contry, continent, subdivisions, timezone]
        apend_list = pd.Series(apend_list, index=col_names)
        my_df = my_df.append(apend_list, ignore_index=True)


    print('the function "find_info_with_ip" has finished working')
    return my_df


if __name__ == '__main__':
    col_names = ['ip', 'country', 'continent', 'subdivisions', 'timezone']
    my_df = pd.DataFrame(columns=col_names)

    df = pd.read_csv('parse_accessLog.csv', sep=';')

    my_df = find_info_with_ip(my_df, df)
    my_df = separation_date_time(my_df, df)
    my_df = find_info_with_request(my_df, df)
    #my_df = status_code_processing(my_df, df) #эсли поле с номером кода будет использован как катеригиональный статус
    my_df['status_code'] = df['%>s']
    #my_df['return_size_object'] = df['%b']
    my_df = copy_size_return_object(my_df, df) #обрабатывается вариант, когда в этом поле содержится не число, а любой другой симпбвол
    my_df = find_info_with_Useragent(my_df, df)


    my_df.to_csv('DictForLearn.csv', sep=';')