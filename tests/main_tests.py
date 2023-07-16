import pytest,main,datetime

def test_check_sidestake():
    empty={}
    assert not main.check_sidestake(empty,'a',2)
    not_enabled={'A':'2'}
    assert not main.check_sidestake(not_enabled,'a',2)
    explicit_disabled={'enablesidestaking':'0'}
    assert not main.check_sidestake(explicit_disabled,'a',2)
    sidestake_1_addr='S5CSzXD3SkTA9xGGpeBtoNJpyryACBR9RD'
    sidestake_1_amount='1'
    sidestake_1=sidestake_1_addr+','+sidestake_1_amount
    sidestake_2_addr='bc3NA8e8E3EoTL1qhRmeprbjWcmuoZ26A2'
    sidestake_2_amount='2'
    sidestake_2=sidestake_2_addr+','+sidestake_2_amount
    enabled={
        'enablesidestaking':'1',
        'sidestake':[sidestake_1,sidestake_2],
    }
    assert main.check_sidestake(enabled,'S5CSzXD3SkTA9xGGpeBtoNJpyryACBR9RD',1) # sidestake should exist
    assert not main.check_sidestake(enabled, 'S5CSzXD3SkTA9xGGpeBtoNJpyryACBR9RD', 2) # sidestake exists but too small
    assert not main.check_sidestake(enabled, 'address_that_doesnt_exist', 2)
def test_global_vars():
    """
    Test to verify various important global vars exist and have sane settings
    @return:
    """
    assert isinstance(main.FORCE_DEV_MODE,bool)
    assert not main.FORCE_DEV_MODE
    assert isinstance(main.BOINC_PROJECT_NAMES,dict)
    assert isinstance(main.DATABASE, dict)
    assert 'TABLE_SLEEP_REASON' in main.DATABASE
    assert 'TABLE_STATUS' in main.DATABASE
def test_combine_dicts():
    dict1={'A':'1'}
    dict2={'B':'1'}
    # verify dicts being combined
    main.combine_dicts(dict1,dict2)
    assert dict1['B']=='1'
    assert dict1['A'] == '1'
    # verify dict2 is taking precedent
    dict1 = {'A': '1'}
    dict2 = {'A': '2'}
    main.combine_dicts(dict1,dict2)
    assert dict1['A']=='2'
def test_resolve_url_boinc_rpc():
    attached_projects={'https://project1.com','http://www.project2.com'}
    attached_projects_dev = {'https://project1.com', 'http://www.PROJECT2.com','http://www.devproject.com'}
    known_boinc_projects=['https://project3.com','http://PROJECT1.com']
    # test that it returns attached projects first
    result=main.resolve_url_boinc_rpc('project1.com',attached_projects,attached_projects_dev,known_boinc_projects,dev_mode=False)
    assert result=='https://project1.com'
    # test that is returns attached dev project before attached regular project, if in dev mode
    result=main.resolve_url_boinc_rpc('project2.com',attached_projects,attached_projects_dev,known_boinc_projects,dev_mode=True)
    assert result=='http://www.PROJECT2.com'
    # test that is returns attached regular project before attached dev project, if in regular mode
    result = main.resolve_url_boinc_rpc('project2.com', attached_projects, attached_projects_dev, known_boinc_projects,dev_mode=False)
    assert result == 'http://www.project2.com'
    # test that it falls back onto known projects if none attached
    result = main.resolve_url_boinc_rpc('project3.com', attached_projects, attached_projects_dev, known_boinc_projects,
                                        dev_mode=False)
    assert result == 'https://project3.com'
@pytest.fixture()
def test_resolve_url_database():
    assert main.resolve_url_database('https://www.boinc.com/myproject')=="BOINC.COM/MYPROJECT"
    assert main.resolve_url_database('http://www.boinc.com/myproject') == "BOINC.COM/MYPROJECT"
    assert main.resolve_url_database('www.boinc.com/myproject') == "BOINC.COM/MYPROJECT"
    assert main.resolve_url_database('https://boinc.com/myproject') == "BOINC.COM/MYPROJECT"
    assert main.resolve_url_database('http://boinc.com/myproject') == "BOINC.COM/MYPROJECT"
def test_resolve_url_list_to_database(test_resolve_url_database):
    url_list=['https://www.boinc.com/myproject','http://boinc.com/myproject']
    assert main.resolve_url_list_to_database(url_list)==["BOINC.COM/MYPROJECT","BOINC.COM/MYPROJECT"]
def test_temp_check():
    # test it only activates when temp control enabled
    main.ENABLE_TEMP_CONTROL=False
    assert main.temp_check()
    # make sure it turns on and off at correct setpoints
    main.ENABLE_TEMP_CONTROL = True
    main.TEMP_COMMAND='echo 67'
    main.START_TEMP=66
    main.STOP_TEMP=70
    assert  main.temp_check()
    main.TEMP_COMMAND = 'echo 77'
    assert not main.temp_check()


# Tests that require a network connection to work. Should be run sparingly for this reason
def test_update_fetch():
    actual_version = main.VERSION
    actual_update_check=main.DATABASE.get('LASTUPDATECHECK')
    update_text="""## Format: Version, SecurityBool (1 or 0), Notes
    ## UPDATE FILE FOR FINDTHEMAG DO NOT DELETE THIS LINE
    1.0,0,Original Version
    2.0,0,Main version
    2.1,0,Update is strongly suggested fixes several major bugs in project handling
    2.2,1,FindTheMag critical security update please see Github for more info
    2.3,0,Various usability improvements and crash fixes
    """
    # assert it finds updates incl security updates
    main.DATABASE['LASTUPDATECHECK']=datetime.datetime(1997,3,3)
    update, security, text = main.update_fetch(update_text,.1)
    assert update
    assert security
    assert text
    # assert no false positives
    main.DATABASE['LASTUPDATECHECK'] = datetime.datetime(1997, 3, 3)
    update, security, text = main.update_fetch(update_text,1000)
    assert not update
    assert not security
    assert not text
    # assert correctly identifying security updates
    main.DATABASE['LASTUPDATECHECK'] = datetime.datetime(1997, 3, 3)
    update,security,text=main.update_fetch(update_text,2.2)
    assert update
    assert not security
    assert text
    # assert not checking too often
    main.DATABASE['LASTUPDATECHECK'] = datetime.datetime.now()
    update,security,text=main.update_fetch(update_text,.1)
    assert not update
    assert not security
    assert not text
    # reset original variables
    main.VERSION = actual_version
    if actual_update_check:
        main.DATABASE['LASTUPDATECHECK']=actual_update_check

