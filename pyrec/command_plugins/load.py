def package_script_load():
    """
    [저장형식]
    Json 형식을 기본으로 한다.
    대상의 최상위 folder에 .pyrec 디렉토리 생성
    디렉토리 안에 file 생성

    1. Script_tree.json은 각 folder를 기준으로 저장
    folder, file의 저장형식
    {“folder1” : {}, “file1” : {}}
    위의 형식으로 최상위 폴더에 대해 저장
    script의 저장형식
    "name":{"type": "file", “location”:’example’, “keyword”:[“example”, “example”], “inscript”:{}}
    # script 안에 script 가 들어가는 경우 inscript 안에 넣어준다.


    2. 키워드 검색을 위해서 keyword_table.json 생성
    저장형식
    {“keyword1”: [{“name”:”ex”, “location”: [“folder1”, “folder2”, “file1”]}, {}, …]}
    """
    return 0

def file_script_load():
    return 0