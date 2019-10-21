import os,sys,time,random
def gen_name(label):
    return "{}-{}".format(label, "".join(random.sample("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRETUVWXYZ",16)))

#---------- env ----------- 
CLEAR_STORAGE_CONTRACTS = {
        "node":"indexer0"
        }

miner_num = 10 if os.environ.get("TEST_ENV", "R") == "R" else 5
CHECK_ENV = {"indexer":"indexer0",
        "bootstrap":"bootstrap0",
        "indexer_num":1,
        "bootstrap_num":1,
        "miner_num":miner_num}

#---------- create bucket ----------- 
POSS_CREATE_BUCKET_PARAM_CHECK_1 = {"bucket": "testbucket123"}
POSS_CREATE_BUCKET_PARAM_CHECK_2 = {"bucket": "", "result":"False"}
POSS_CREATE_BUCKET_PARAM_CHECK_3 = {"bucket": "/", "result":"False"}
POSS_CREATE_BUCKET_PARAM_CHECK_4 = {"bucket": "//", "result":"False"}
POSS_CREATE_BUCKET_PARAM_CHECK_5 = {"bucket": "_bucket", "result":"False"}
POSS_CREATE_BUCKET_PARAM_CHECK_6 = {"bucket": "123_bucket", "result":"False"}
POSS_CREATE_BUCKET_PARAM_CHECK_7 = {"bucket": "/bucket", "result":"False"}
POSS_CREATE_BUCKET_PARAM_CHECK_8 = {"bucket": "?><{}[]()-=_+", "result":"False"}

#---------- create same bucket ----------- 
POSS_CREATE_SAME_BUCKET = {
        "first": {"bucket": "testbucketsame"},
        "second": {"bucket": "testbucketsame", "result":"False"}
        }

#---------- create same bucket ----------- 
tmp = gen_name("1K")
POSS_DELETE_NOT_EMPTY_BUCKET = {
        "put": {"bucket": "testbucketdelete", "key":tmp, "body": "1K"},
        "delete": {"bucket": "testbucketdelete", "result": "False"}
        }

#---------- delete bucket ----------- 
POSS_DELETE_BUCKET_PARAM_CHECK_1 = {"bucket": "./", "result":"False"}
POSS_DELETE_BUCKET_PARAM_CHECK_2 = {"bucket": "../", "result":"False"}
POSS_DELETE_BUCKET_PARAM_CHECK_3 = {"bucket": "not_exists", "result":"False"}

#---------- put object ----------- 
tmp = gen_name("dir")
CREATE_DIR = {"key": tmp, "isdir": "True"}

POSS_PUT_PARAMETER_CHECK_FILE_PREPARE = {"key":"test_object", "body": "1K"}

tmp = gen_name("not")
POSS_PUT_PARAMETER_CHECK_FILE_NOT_FOUND = {"key":tmp, "body": "not_exists", "result":"False"}

tmp = gen_name("1K")
POSS_PUT_PARAMETER_CHECK_EMPTY_CHIPRICE = {"key":tmp, "body": "1K", "chiprice":"", "result":"False"}

tmp = gen_name("1K")
POSS_PUT_PARAMETER_CHECK_ZERO_CHIPRICE = {"key":tmp, "body": "1K", "chiprice":"0", "result":"False"}

tmp = gen_name("1K")
POSS_PUT_PARAMETER_CHECK_NEGATIVE_CHIPRICE = {"key":tmp, "body": "1K", "chiprice":"-1", "result":"False"}

tmp = gen_name("1K")
POSS_PUT_PARAMETER_CHECK_STR_CHIPRICE = {"key":tmp, "body": "1K", "chiprice":"abc", "result":"False"}

tmp = gen_name("1K")
POSS_PUT_PARAMETER_CHECK_EMPTY_COPIES = {"key":tmp, "body": "1K", "copies":"", "result":"False"}

tmp = gen_name("1K")
POSS_PUT_PARAMETER_CHECK_ZERO_COPIES = {"key":tmp, "body": "1K", "copies":0, "result":"False"}

tmp = gen_name("1K")
POSS_PUT_PARAMETER_CHECK_NEGATIVE_COPIES = {"key":tmp, "body": "1K", "copies":-1, "result":"False"}

tmp = gen_name("1K")
POSS_PUT_PARAMETER_CHECK_STR_COPIES = {"key":tmp, "body": "1K", "copies":"abc", "result":"False"}

tmp = gen_name("1K")
POSS_PUT_PARAMETER_CHECK_EMPTY_EXPIRES = {"key":tmp, "body": "1K", "expires":"", "result":"False"}

tmp = gen_name("1K")
POSS_PUT_PARAMETER_CHECK_ZERO_EXPIRES = {"key":tmp, "body": "1K", "expires":"0", "result":"False"}

tmp = gen_name("1K")
POSS_PUT_PARAMETER_CHECK_NEGATIVE_EXPIRES = {"key":tmp, "body": "1K", "expires":"-1", "result":"False"}

tmp = gen_name("1K")
POSS_PUT_PARAMETER_CHECK_STR_EXPIRES = {"key":tmp, "body": "1K", "expires":"abc", "result":"False"}

#---------- get object ----------- 

POSS_GET_PARAMETER_CHECK_EMPTY_CHIPRICE = {"key":"test_object", "chiprice":"", "result":"False"}
POSS_GET_PARAMETER_CHECK_ZERO_CHIPRICE = {"key":"test_object", "chiprice":"0", "result":"False"}
POSS_GET_PARAMETER_CHECK_NEGATIVE_CHIPRICE = {"key":"test_object", "chiprice":"-1", "result":"False"}
POSS_GET_PARAMETER_CHECK_STR_CHIPRICE = {"key":"test_object", "chiprice":"abc", "result":"False"}
POSS_GET_PARAMETER_CHECK_LOW_CHIPRICE = {"key":"test_object", "chiprice":"30", "result":"False"}

#---------- delete object ----------- 
POSS_DELETE_PARAMETER_CHECK_ERROR_BUCKET = {"bucket":"not_exist", "key":"test_object", "result":"False"}
POSS_DELETE_PARAMETER_CHECK_ERROR_KEY_1 = {"key":"not_exist", "result":"False"}
POSS_DELETE_PARAMETER_CHECK_ERROR_KEY_2 = {"key":"/", "result":"False"}
POSS_DELETE_PARAMETER_CHECK_ERROR_KEY_3 = {"key":"../", "result":"False"}
POSS_DELETE_PARAMETER_CHECK_ERROR_KEY_4 = {"key":"", "result":"False"}

#---------- share object ----------- 
POSS_SHARE_PARAMETER_CHECK_ERROR_BUCKET = {"bucket":"not_exist", "key":"test_object", "result":"False"}
POSS_SHARE_PARAMETER_CHECK_SHARE_DIR = {"key":"test_dir", "result":"False"}
POSS_SHARE_PARAMETER_CHECK_ERROR_KEY_1 = {"key":"not_exist", "result":"False"}
POSS_SHARE_PARAMETER_CHECK_ERROR_KEY_2 = {"key":"/", "result":"False"}
POSS_SHARE_PARAMETER_CHECK_ERROR_KEY_3 = {"key":"../", "result":"False"}
POSS_SHARE_PARAMETER_CHECK_ERROR_KEY_4 = {"key":"", "result":"False"}

#---------- renew object ----------- 
POSS_RENEW_PARAMETER_CHECK_ERROR_BUCKET = {"bucket":"not_exist", "key":"test_object", "result":"False"}
POSS_RENEW_PARAMETER_CHECK_ERROR_KEY = {"key":"not_exist", "result":"False"}
POSS_RENEW_PARAMETER_CHECK_ERROR_CHIPRICE_1 = {"key":"test_object", "chiprice":"0", "result":"False"}
POSS_RENEW_PARAMETER_CHECK_ERROR_CHIPRICE_2 = {"key":"test_object", "chiprice":"-1", "result":"False"}
POSS_RENEW_PARAMETER_CHECK_ERROR_CHIPRICE_3 = {"key":"test_object", "chiprice":"abc", "result":"False"}
POSS_RENEW_PARAMETER_CHECK_ERROR_COPIES_1 = {"key":"test_object", "copies":0, "result":"False"}
POSS_RENEW_PARAMETER_CHECK_ERROR_COPIES_2 = {"key":"test_object", "copies":-1, "result":"False"}
POSS_RENEW_PARAMETER_CHECK_ERROR_COPIES_3 = {"key":"test_object", "copies":"abc", "result":"False"}
POSS_RENEW_PARAMETER_CHECK_ERROR_EXPIRES_1 = {"key":"test_object", "expires":"2018-01-01", "result":"False"}
POSS_RENEW_PARAMETER_CHECK_ERROR_EXPIRES_2 = {"key":"test_object", "expires":"2118-01-01", "result":"False"}
POSS_RENEW_PARAMETER_CHECK_ERROR_EXPIRES_3 = {"key":"test_object", "expires":"abc", "result":"False"}

#---------- copy object ----------- 
POSS_COPY_PARAMETER_CHECK_ERROR_KEY = {"key":"", "source":"tstbucket/test_object", "result":"False"}
POSS_COPY_PARAMETER_CHECK_ERROR_SOURCE = {"key":"test_object_copy", "source":"ttbucket/test_object", "result":"False"}
POSS_COPY_PARAMETER_CHECK_ERROR_CHIPRICE = {"key":"test_object_copy", "source":"tstbucket/test_object", "chiprice":"10", "result":"False"}
POSS_COPY_PARAMETER_CHECK_ERROR_COPIES = {"key":"test_object_copy", "source":"tstbucket/test_object", "copies":0, "result":"False"}
POSS_COPY_PARAMETER_CHECK_ERROR_EXPIRES = {"key":"test_object_copy", "source":"tstbucket/test_object", "expires":"2018-01-01", "result":"False"}

#---------- put get delete ----------- 
tmp = gen_name("1K")
POSS_PUT_GET_DELETE_1K = {
        "put" : {"key":tmp, "body": "1K"},
        "get" : {"key":tmp, "outfile":tmp},
        "delete" : {"key":tmp}
        }

tmp = gen_name("16lessM")
POSS_PUT_GET_DELETE_16LESSM = {
        "put" : {"key":tmp, "body": "16lessM"},
        "get" : {"key":tmp, "outfile":tmp},
        "delete" : {"key":tmp}
        }

tmp = gen_name("16largerM")
POSS_PUT_GET_DELETE_16LARGERM = {
        "put" : {"key":tmp, "body": "16largerM"},
        "get" : {"key":tmp, "outfile":tmp},
        "delete" : {"key":tmp}
        }

tmp = gen_name("32M")
POSS_PUT_GET_DELETE_32M_2COPIES = {
        "put" : {"key":tmp, "body": "32M", "copies": 2},
        "get" : {"key":tmp, "outfile":tmp},
        "delete" : {"key":tmp}
        }

#---------- put move get delete ----------- 
tmp = gen_name("1K")
POSS_PUT_MOVE_GET_DELETE_1K = {
        "put" : {"key":tmp, "body": "1K"},
        "move" : {"key":tmp+"move", "source": "tstbucket/"+tmp},
        "get" : {"key":tmp+"move", "outfile":tmp+"move"},
        "delete" : {"key":tmp+"move"}
        }

tmp = gen_name("1K")
POSS_PUT_MOVE_GET_DELETE_1K_2COPIES = {
        "put" : {"key":tmp, "body": "1K", "copies": 2},
        "move" : {"key":tmp+"move", "source": "tstbucket/"+tmp},
        "get" : {"key":tmp+"move", "outfile":tmp+"move"},
        "delete" : {"key":tmp+"move"}
        }

tmp = gen_name("1K")
POSS_PUT_MOVE_GET_DELETE_1K_2COPIES_BETWEEN_BUCKETS = {
        "put" : {"key":tmp, "body": "1K", "copies": 2},
        "move" : {"bucket":"tstbucketmove", "key":tmp+"move", "source": "tstbucket/"+tmp},
        "get" : {"bucket":"tstbucketmove", "key":tmp+"move", "outfile":tmp+"move"},
        "delete" : {"bucket":"tstbucketmove", "key":tmp+"move"}
        }

tmp = gen_name("32M")
POSS_PUT_MOVE_GET_DELETE_32M_2COPIES_BETWEEN_BUCKETS = {
        "put" : {"key":tmp, "body": "32M"},
        "move" : {"bucket":"tstbucketmove", "key":tmp+"move", "source": "tstbucket/"+tmp},
        "get" : {"bucket":"tstbucketmove", "key":tmp+"move", "outfile":tmp+"move"},
        "delete" : {"bucket":"tstbucketmove", "key":tmp+"move"}
        }

#---------- put share get delete get ----------- 
tmp = gen_name("1K")
POSS_PUT_SHARE_GET_DELETE_GET_1K = {
        "put" : {"key":tmp, "body": "1K"},
        "get" : {"node":"poss1", "bucket":"", "outfile":tmp},
        "delete" : {"key":tmp},
        "failget" : {"node":"poss1", "bucket":"", "outfile":tmp, "result": "False"}
        }

tmp = gen_name("32M")
POSS_PUT_SHARE_GET_DELETE_GET_32M_2COPIES = {
        "put" : {"key":tmp, "body": "32M","copies":2},
        "get" : {"node":"poss1", "bucket":"", "outfile":tmp},
        "delete" : {"key":tmp},
        "failget" : {"node":"poss1", "bucket":"", "outfile":tmp, "result": "False"}
        }

#---------- put move share get delete ----------- 
tmp = gen_name("1K")
POSS_PUT_MOVE_SHARE_GET_DELETE_1K = {
        "put" : {"key":tmp, "body": "1K"},
        "move" : {"bucket":"tstbucketmove", "key":tmp+"move", "source": "tstbucket/"+tmp},
        "get" : {"node":"poss1", "bucket":"", "key":"", "outfile":tmp+"move"},
        "delete" : {"bucket":"tstbucketmove", "key":tmp+"move"},
        }

tmp = gen_name("32M")
POSS_PUT_MOVE_SHARE_GET_DELETE_32M_2COPIES = {
        "put" : {"key":tmp, "body": "32M"},
        "move" : {"bucket":"tstbucketmove", "key":tmp+"move", "source": "tstbucket/"+tmp},
        "get" : {"node":"poss1", "bucket":"", "outfile":tmp+"move"},
        "delete" : {"bucket":"tstbucketmove", "key":tmp+"move"},
        }

#---------- put copy get delete ----------- 
tmp = gen_name("1K")
POSS_PUT_COPY_GET_DELETE_1K = {
        "put" : {"key":tmp, "body": "1K"},
        "copy" : {"key":tmp+"copy", "source": "tstbucket/"+tmp},
        "get" : {"key":tmp+"copy", "outfile":tmp+"copy"},
        }

tmp = gen_name("32M")
POSS_PUT_COPY_GET_DELETE_32M = {
        "put" : {"key":tmp, "body": "32M"},
        "copy" : {"key":tmp+"copy", "source": "tstbucket/"+tmp},
        "get" : {"key":tmp+"copy", "outfile":tmp+"copy"},
        }

tmp = gen_name("1K")
POSS_PUT_COPY_GET_DELETE_1K_2COPIES_BETWEEN_BUCKETS = {
        "put" : {"key":tmp, "body": "1K", "copies":2},
        "copy" : {"bucket":"tstbucketcopy", "key":tmp+"copy", "source": "tstbucket/"+tmp, "copies":2},
        "get" : {"bucket":"tstbucketcopy", "key":tmp+"copy", "outfile":tmp+"copy"},
        }

tmp = gen_name("32M")
POSS_PUT_COPY_GET_DELETE_32M_2COPIES_BETWEEN_BUCKETS = {
        "put" : {"key":tmp, "body": "32M", "copies":2},
        "copy" : {"bucket":"tstbucketcopy", "key":tmp+"copy", "source": "tstbucket/"+tmp, "copies":2},
        "get" : {"bucket":"tstbucketcopy", "key":tmp+"copy", "outfile":tmp+"copy"},
        }

#---------- put move copy get delete ----------- 
tmp = gen_name("1K")
POSS_PUT_MOVE_COPY_GET_DELETE_1K = {
        "put" : {"key":tmp, "body": "1K"},
        "move" : {"key":tmp+"move", "source": "tstbucket/"+tmp},
        "copy" : {"key":tmp+"copy", "source":"tstbucket/"+tmp+"move"},
        "get" : {"key":tmp+"copy"}
        }

tmp = gen_name("1K")
POSS_PUT_MOVE_COPY_GET_DELETE_1K_2COPIES = {
        "put" : {"key":tmp, "body": "1K","copies":2},
        "move" : {"key":tmp+"move", "source": "tstbucket/"+tmp},
        "copy" : {"key":tmp+"copy", "source":"tstbucket/"+tmp+"move", "copies":2},
        "get" : {"key":tmp+"copy"}
        }

tmp = gen_name("32M")
POSS_PUT_MOVE_COPY_GET_DELETE_32M = {
        "put" : {"key":tmp, "body": "32M"},
        "move" : {"key":tmp+"move", "source": "tstbucket/"+tmp},
        "copy" : {"key":tmp+"copy", "source":"tstbucket/"+tmp+"move"},
        "get" : {"key":tmp+"copy"}
        }

tmp = gen_name("32M")
POSS_PUT_MOVE_COPY_GET_DELETE_32M_2COPIES = {
        "put" : {"key":tmp, "body": "32M","copies":2},
        "move" : {"key":tmp+"move", "source": "tstbucket/"+tmp},
        "copy" : {"key":tmp+"copy", "source":"tstbucket/"+tmp+"move", "copies":2},
        "get" : {"key":tmp+"copy"}
        }

#---------- put copy move get delete ----------- 
tmp = gen_name("1K")
POSS_PUT_COPY_MOVE_GET_DELETE_1K = {
        "put" : {"key":tmp, "body": "1K"},
        "copy" : {"key":tmp+"copy", "source":"tstbucket/"+tmp},
        "move" : {"key":tmp+"move", "source": "tstbucket/"+tmp+"copy"},
        "get" : {"key":tmp+"move"}
        }

tmp = gen_name("1K")
POSS_PUT_COPY_MOVE_GET_DELETE_1K_2COPIES = {
        "put" : {"key":tmp, "body": "1K","copies":2},
        "copy" : {"key":tmp+"copy", "source":"tstbucket/"+tmp, "copies":2},
        "move" : {"key":tmp+"move", "source": "tstbucket/"+tmp+"copy"},
        "get" : {"key":tmp+"move"}
        }

tmp = gen_name("32M")
POSS_PUT_COPY_MOVE_GET_DELETE_32M = {
        "put" : {"key":tmp, "body": "32M"},
        "copy" : {"key":tmp+"copy", "source":"tstbucket/"+tmp},
        "move" : {"key":tmp+"move", "source": "tstbucket/"+tmp+"copy"},
        "get" : {"key":tmp+"move"}
        }

tmp = gen_name("32M")
POSS_PUT_COPY_MOVE_GET_DELETE_32M_2COPIES = {
        "put" : {"key":tmp, "body": "32M","copies":2},
        "copy" : {"key":tmp+"copy", "source":"tstbucket/"+tmp, "copies":2},
        "move" : {"key":tmp+"move", "source": "tstbucket/"+tmp+"copy"},
        "get" : {"key":tmp+"move"}
        }

#---------- put renew get delete ----------- 
tmp = gen_name("1K")
POSS_PUT_RENEW_GET_DELETE_1K_INCREATE_CHIPRICE_COPIES_EXPIRES = {
        "put" : {"key":tmp, "body": "1K"},
        "renew" : {"key":tmp, "copies": 2, "chiprice":"210", "expires":"2020-01-01"},
        "get": {"key":tmp}
        }

tmp = gen_name("32M")
POSS_PUT_RENEW_GET_DELETE_32M_INCREATE_CHIPRICE_COPIES_EXPIRES = {
        "put" : {"key":tmp, "body": "32M"},
        "renew" : {"key":tmp, "copies": 2, "chiprice":"210", "expires":"2020-01-01"},
        "get": {"key":tmp}
        }

tmp = gen_name("1K")
POSS_PUT_RENEW_GET_DELETE_1K_DECREASE_COPIES = {
        "put" : {"key":tmp, "body": "1K", "copies": 2},
        "renew" : {"key":tmp, "copies": 1, "expires":"2020-01-01"},
        "get": {"key":tmp}
        }

tmp = gen_name("32M")
POSS_PUT_RENEW_GET_DELETE_32M_DECREASE_COPIES = {
        "put" : {"key":tmp, "body": "32M", "copies": 2},
        "renew" : {"key":tmp, "copies": 1, "expires":"2020-01-01"},
        "get": {"key":tmp}
        }

tmp = gen_name("1K")
POSS_PUT_RENEW_GET_DELETE_1K_DECREASE_CHIPRICE = {
        "put" : {"key":tmp, "body": "1K", "chiprice": "300"},
        "renew" : {"key":tmp, "chiprice": "200", "expires":"2020-01-01"},
        "get": {"key":tmp}
        }

tmp = gen_name("32M")
POSS_PUT_RENEW_GET_DELETE_32M_DECREASE_CHIPRICE = {
        "put" : {"key":tmp, "body": "32M", "chiprice": "300"},
        "renew" : {"key":tmp, "chiprice": "200", "expires":"2020-01-01"},
        "get": {"key":tmp}
        }

#---------- put renew move get delete ----------- 
tmp = gen_name("1K")
POSS_PUT_RENEW_MOVE_GET_DELETE_1K = {
        "put" : {"key":tmp, "body": "1K"},
        "renew" : {"key":tmp, "chiprice": "210", "copies": 1, "expires":"2020-01-01"},
        "move" : {"key":tmp+"move", "source":"tstbucket/"+tmp},
        "get" : {"key":tmp+"move"}
        }

tmp = gen_name("32M")
POSS_PUT_RENEW_MOVE_GET_DELETE_32M = {
        "put" : {"key":tmp, "body": "32M"},
        "renew" : {"key":tmp, "chiprice": "210", "copies": 1, "expires":"2020-01-01"},
        "move" : {"key":tmp+"move", "source":"tstbucket/"+tmp},
        "get" : {"key":tmp+"move"}
        }

#---------- put renew copy get delete ----------- 
tmp = gen_name("1K")
POSS_PUT_RENEW_COPY_GET_DELETE_1K = {
        "put" : {"key":tmp, "body": "1K"},
        "renew" : {"key":tmp, "chiprice": "210", "copies": 1, "expires":"2020-01-01"},
        "copy" : {"key":tmp+"copy", "source":"tstbucket/"+tmp},
        "get" : {"key":tmp+"copy"}
        }

tmp = gen_name("32M")
POSS_PUT_RENEW_COPY_GET_DELETE_32M = {
        "put" : {"key":tmp, "body": "32M"},
        "renew" : {"key":tmp, "chiprice": "210", "copies": 1, "expires":"2020-01-01"},
        "copy" : {"key":tmp+"copy", "source":"tstbucket/"+tmp},
        "get" : {"key":tmp+"copy"}
        }

#---------- put pause resume get delete ----------- 
tmp = gen_name("64M")
POSS_PUT_PAUSE_RESUME_GET_DELETE_64M_25 = {
        "put" : {"key":tmp, "body": "64M","sync":"False"},
        "pause" : {"condition": 25.0},
        "get" : {"key":tmp}
        }

tmp = gen_name("64M")
POSS_PUT_PAUSE_RESUME_GET_DELETE_64M_2COPIES_25 = {
        "put" : {"key":tmp, "body": "64M", "copies":2, "sync":"False"},
        "pause" : {"condition": 25.0},
        "get" : {"key":tmp}
        }

tmp = gen_name("64M")
POSS_PUT_PAUSE_RESUME_GET_DELETE_64M_50 = {
        "put" : {"key":tmp, "body": "64M","sync":"False"},
        "pause" : {"condition": 50.0},
        "get" : {"key":tmp}
        }

tmp = gen_name("64M")
POSS_PUT_PAUSE_RESUME_GET_DELETE_64M_2COPIES_50 = {
        "put" : {"key":tmp, "body": "64M", "copies":2, "sync":"False"},
        "pause" : {"condition": 50.0},
        "get" : {"key":tmp}
        }


#---------- put get pause resume delete ----------- 
tmp = gen_name("64M")
POSS_PUT_GET_PAUSE_RESUME_DELETE_64M_25 = {
        "put" : {"key":tmp, "body": "64M"},
        "get" : {"key":tmp, "sync":"False"},
        "pause" : {"condition": 25.0},
        }

tmp = gen_name("128M")
POSS_PUT_GET_PAUSE_RESUME_DELETE_128M_50 = {
        "put" : {"key":tmp, "body": "128M"},
        "get" : {"key":tmp, "sync":"False"},
        "pause" : {"condition": 50.0},
        }

#---------- put share get pause resume delete ----------- 
tmp = gen_name("64M")
POSS_PUT_SHARE_GET_PAUSE_RESUME_DELETE_64M_25 = {
        "put" : {"key":tmp, "body": "64M"},
        "get" : {"node":"poss1", "bucket":"", "sync":"False"},
        "pause" : {"node":"poss1", "condition": 25.0}
        }

tmp = gen_name("128M")
POSS_PUT_SHARE_GET_PAUSE_RESUME_DELETE_128M_50 = {
        "put" : {"key":tmp, "body": "128M"},
        "get" : {"node":"poss1", "bucket":"", "sync":"False"},
        "pause" : {"node":"poss1", "condition": 50.0}
        }

#---------- put copy pause resume get delete ----------- 
tmp = gen_name("64M")
POSS_PUT_COPY_PAUSE_RESUME_GET_DELETE_64M_25 = {
        "put" : {"key":tmp, "body": "64M"},
        "copy" : {"key":tmp+"copy", "source": "tstbucket/"+tmp, "sync":"False"},
        "pause" : {"condition": 25.0},
        "get" : {"key":tmp+"copy"}
        }

tmp = gen_name("128M")
POSS_PUT_COPY_PAUSE_RESUME_GET_DELETE_128M_55 = {
        "put" : {"key":tmp, "body": "64M"},
        "copy" : {"key":tmp+"copy", "source": "tstbucket/"+tmp, "sync":"False"},
        "pause" : {"condition": 55.0},
        "get" : {"key":tmp+"copy"}
        }

#---------- import export delete ----------- 
PPIO_IMPORT_EXPORT_DELETE_288B = {"import" : {"path": "288B"}}
PPIO_IMPORT_EXPORT_DELETE_1K = {"import" : {"path": "1K"}}
PPIO_IMPORT_EXPORT_DELETE_16LESSM = {"import" : {"path": "16lessM"}}
PPIO_IMPORT_EXPORT_DELETE_16M = {"import" : {"path": "16M"}}
PPIO_IMPORT_EXPORT_DELETE_16LARGERM = {"import" : {"path": "16largerM"}}
PPIO_IMPORT_EXPORT_DELETE_256M = {"import" : {"path": "256M"}}

#---------- import put get export delete ----------- 
PPIO_PUT_GET_EXPORT_DELETE_288B = {"import" : {"path": "288B"}}
PPIO_PUT_GET_EXPORT_DELETE_1K = {"import" : {"path": "1K"}}
PPIO_PUT_GET_EXPORT_DELETE_16LESSM = {"import" : {"path": "16lessM"}}
PPIO_PUT_GET_EXPORT_DELETE_16M = {"import" : {"path": "16M"}}
PPIO_PUT_GET_EXPORT_DELETE_16LARGERM = {"import" : {"path": "16largerM"}}
PPIO_PUT_GET_EXPORT_DELETE_256M = {"import" : {"path": "256M"}}

PPIO_PUT_GET_EXPORT_DELETE_288B_BETWEEN_PPIO = {
        "import" : {"path": "288B"},
        "get": {"node":"ppio1"},
        }
PPIO_PUT_GET_EXPORT_DELETE_1K_BETWEEN_PPIO = {
        "import" : {"path": "1K"},
        "get": {"node":"ppio1"},
        }
PPIO_PUT_GET_EXPORT_DELETE_16LESSM_BETWEEN_PPIO = {
        "import" : {"path": "16lessM"},
        "get": {"node":"ppio1"},
        }
PPIO_PUT_GET_EXPORT_DELETE_16M_BETWEEN_PPIO = {
        "import" : {"path": "16M"},
        "get": {"node":"ppio1"},
        }
PPIO_PUT_GET_EXPORT_DELETE_16LARGERM_BETWEEN_PPIO = {
        "import" : {"path": "16largerM"},
        "get": {"node":"ppio1"},
        }
PPIO_PUT_GET_EXPORT_DELETE_256M_BETWEEN_PPIO = {
        "import" : {"path": "256M"},
        "get": {"node":"ppio1"},
        }

#---------- import put renew get export delete file ----------- 
PPIO_PUT_RENEW_GET_EXPORT_DELETE_288B = {
        "import" : {"path": "288B"},
        "renew" : {"chiprice": "210"},
        }

PPIO_PUT_RENEW_GET_EXPORT_DELETE_16LESSM = {
        "import" : {"path": "16lessM"},
        "renew" : {"chiprice": "210"},
        }

PPIO_PUT_RENEW_GET_EXPORT_DELETE_16M = {
        "import" : {"path": "16M"},
        "renew" : {"chiprice": "210"},
        }

PPIO_PUT_RENEW_GET_EXPORT_DELETE_16LARGERM = {
        "import" : {"path": "16largerM"},
        "renew" : {"chiprice": "210"},
        }

#---------- import put renew get export delete same chi ----------- 
PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_INC_COPY_DEC_CHI_TEST = {
        "import" : {"path": "1K"},
        "put" : {"copies":1, "chiprice":"140"},
        "renew": {"chiprice":"110", "copies":2}
        }

PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_DEC_COPY = {
        "import" : {"path": "1K"},
        "put" : {"path": "1K", "copies":2},
        }

PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_INC_COPY = {
        "import" : {"path": "1K"},
        "renew" : {"copies":2},
        }

PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_DEC_COPY_EXPIRE = {
        "import" : {"path": "1K"},
        "put" : {"copies":2, "duration":172800},
        "renew" : {"result":"False"},
        }

PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_DEC_COPY_INC_EXPIRE = {
        "import" : {"path": "1K", "copies":2},
        "put" : {"copies":2},
        "renew" : {"duration": 172800},
        }

PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_DEC_EXPIRE_INC_COPY = {
        "import" : {"path": "1K"},
        "put" : {"duration":172800},
        "renew" : {"copies":2, "result":"False"},
        }

PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_INC_COPY_EXPIRE = {
        "import" : {"path": "1K"},
        "renew" : {"copies":2, "duration":172800},
        }

#---------- import put renew get export delete inc chi ----------- 
PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_INC_CHI = {
        "import" : {"path": "1K"},
        "renew" : {"chiprice": "210"},
        }

PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_INC_CHI_COPY = {
        "import" : {"path": "1K"},
        "renew" : {"chiprice": "210", "copies":2},
        }

PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_INC_CHI_COPY_EXPIRE = {
        "import" : {"path": "1K"},
        "renew" : {"chiprice": "210", "copies":2, "duration":172800},
        }

PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_INC_CHI_COPY_DEC_EXPIRE = {
        "import" : {"path": "1K"},
        "put" : {"duration":172800},
        "renew" : {"chiprice": "210", "copies":2, "duration": 86400, "result":"False"},
        }

PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_INC_CHI_DEC_COPY = {
        "import" : {"path": "1K"},
        "put" : {"copies":2},
        "renew" : {"chiprice": "210"},
        }

PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_INC_CHI_EXPIRE_DEC_COPY = {
        "import" : {"path": "1K"},
        "put" : {"copies":2},
        "renew" : {"chiprice": "210", "duration":172800},
        }

PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_INC_CHI_DEC_COPY_EXPIRE = {
        "import" : {"path": "1K"},
        "put" : {"copies":2, "duration":172800},
        "renew" : {"chiprice": "210", "duration": 86400, "result":"False"},
        }

#---------- import put renew get export delete dec chi ----------- 
PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_DEC_CHI = {
        "import" : {"path": "1K"},
        "put" : {"chiprice": "300"},
        "renew" : {"chiprice": "210"},
        }

PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_DEC_CHI_COPY = {
        "import" : {"path": "1K"},
        "put" : {"chiprice": "300", "copies":2},
        "renew" : {"chiprice": "210"},
        }

PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_DEC_CHI_INC_COPY = {
        "import" : {"path": "1K"},
        "put" : {"chiprice": "300"},
        "renew" : {"chiprice": "210", "copies":2},
        }

PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_DEC_CHI_COPY_EXPIRE = {
        "import" : {"path": "1K"},
        "put" : {"chiprice": "300", "copies":2, "duration":172800},
        "renew" : {"chiprice": "210", "result":"False"},
        }

PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_DEC_CHI_COPY_INC_EXPIRE = {
        "import" : {"path": "1K"},
        "put" : {"chiprice": "300", "copies":2},
        "renew" : {"chiprice": "210", "duration": 172800},
        }

PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_DEC_CHI_EXPIRE_INC_COPY = {
        "import" : {"path": "1K"},
        "put" : {"chiprice": "300", "duration":172800},
        "renew" : {"chiprice": "210", "copies":2, "result":"False"},
        }

PPIO_PUT_RENEW_GET_EXPORT_DELETE_1K_DEC_CHI_INC_COPY_EXPIRE = {
        "import" : {"path": "1K"},
        "put" : {"chiprice": "300"},
        "renew" : {"chiprice": "210", "copies":2, "duration":172800},
        }

#---------- miner will leave ----------- 
tmp = gen_name("1K")
copies = 10 if os.environ.get("TEST_ENV", "R") == "R" else 3
MINER_WILL_LEAVE = {
        "willleave":{},
        "put" : {"key":tmp, "body": "1K", "copies":copies},
        }

#---------- miner clear chunks ----------- 
MINER_CLEAR_CHUNKS_0 = {
        "indexer":{"node":"indexer0"},
        "miner":{"node":"miner0"}
        }

MINER_CLEAR_CHUNKS_1 = {
        "indexer":{"node":"indexer0"},
        "miner":{"node":"miner1"}
        }

#---------- indexer reschedaul ----------- 
tmp = gen_name("1K")
INDEXER_RESCHEDUAL = {
        "put1" : {"key":tmp+"1", "body": "1K","chiprice":"100", "copies":2},
        "put2" : {"key":tmp+"2", "body": "1K","chiprice":"100", "copies":2},
        "renew": {"key":tmp+"1", "chiprice":"150"},
        "stop1": {"node":"miner0"},
        "check1": {"key":tmp+"2", "state":"Part-Deal"},
        "put3" : {"key":tmp+"3", "body": "1K","chiprice":"100", "copies":2, "result":"False"},
        "check2": {"key":tmp+"1", "state":"Deal"},
        "stop2": {"node":"miner1"},
        "check2": {"key":tmp+"2", "state":"Bid"},
        }
