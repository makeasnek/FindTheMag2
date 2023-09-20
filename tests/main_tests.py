import sys
import os

sys.path.append(os.getcwd() + '/..')

import json

import pytest, main, datetime
from typing import Dict, List, Union, Any, Tuple


def test_check_sidestake_original():
    empty = {}
    assert not main.check_sidestake(empty, "a", 2)
    not_enabled = {"A": "2"}
    assert not main.check_sidestake(not_enabled, "a", 2)
    explicit_disabled = {"enablesidestaking": "0"}
    assert not main.check_sidestake(explicit_disabled, "a", 2)
    sidestake_1_addr = "S5CSzXD3SkTA9xGGpeBtoNJpyryACBR9RD"
    sidestake_1_amount = "1"
    sidestake_1 = sidestake_1_addr + "," + sidestake_1_amount
    sidestake_2_addr = "bc3NA8e8E3EoTL1qhRmeprbjWcmuoZ26A2"
    sidestake_2_amount = "2"
    sidestake_2 = sidestake_2_addr + "," + sidestake_2_amount
    enabled = {
        "enablesidestaking": "1",
        "sidestake": [sidestake_1, sidestake_2],
    }
    assert main.check_sidestake(
        enabled, "S5CSzXD3SkTA9xGGpeBtoNJpyryACBR9RD", 1
    )  # sidestake should exist
    assert not main.check_sidestake(
        enabled, "S5CSzXD3SkTA9xGGpeBtoNJpyryACBR9RD", 2
    )  # sidestake exists but too small
    assert not main.check_sidestake(enabled, "address_that_doesnt_exist", 2)


def test_global_vars():
    """
    Test to verify various important global vars exist and have sane settings
    @return:
    """
    assert isinstance(main.FORCE_DEV_MODE, bool)
    assert not main.FORCE_DEV_MODE
    assert isinstance(main.BOINC_PROJECT_NAMES, dict)
    assert isinstance(main.DATABASE, dict)
    assert "TABLE_SLEEP_REASON" in main.DATABASE
    assert "TABLE_STATUS" in main.DATABASE


def test_combine_dicts():
    dict1 = {"A": "1"}
    dict2 = {"B": "1"}
    # verify dicts being combined
    main.combine_dicts(dict1, dict2)
    assert dict1["B"] == "1"
    assert dict1["A"] == "1"
    # verify dict2 is taking precedent
    dict1 = {"A": "1"}
    dict2 = {"A": "2"}
    main.combine_dicts(dict1, dict2)
    assert dict1["A"] == "2"


def test_resolve_url_boinc_rpc():
    attached_projects = {"https://project1.com", "http://www.project2.com"}
    attached_projects_dev = {
        "https://project1.com",
        "http://www.PROJECT2.com",
        "http://www.devproject.com",
    }
    known_boinc_projects = ["https://project3.com", "http://PROJECT1.com"]
    # test that it returns attached projects first
    result = main.resolve_url_boinc_rpc(
        "project1.com",
        attached_projects,
        attached_projects_dev,
        known_boinc_projects,
        dev_mode=False,
    )
    assert result == "https://project1.com"
    # test that is returns attached dev project before attached regular project, if in dev mode
    result = main.resolve_url_boinc_rpc(
        "project2.com",
        attached_projects,
        attached_projects_dev,
        known_boinc_projects,
        dev_mode=True,
    )
    assert result == "http://www.PROJECT2.com"
    # test that is returns attached regular project before attached dev project, if in regular mode
    result = main.resolve_url_boinc_rpc(
        "project2.com",
        attached_projects,
        attached_projects_dev,
        known_boinc_projects,
        dev_mode=False,
    )
    assert result == "http://www.project2.com"
    # test that it falls back onto known projects if none attached
    result = main.resolve_url_boinc_rpc(
        "project3.com",
        attached_projects,
        attached_projects_dev,
        known_boinc_projects,
        dev_mode=False,
    )
    assert result == "https://project3.com"


def test_resolve_url_database():
    assert (
        main.resolve_url_database("https://www.boinc.com/myproject")
        == "BOINC.COM/MYPROJECT"
    )
    assert (
        main.resolve_url_database("http://www.boinc.com/myproject")
        == "BOINC.COM/MYPROJECT"
    )
    assert main.resolve_url_database("www.boinc.com/myproject") == "BOINC.COM/MYPROJECT"
    assert (
        main.resolve_url_database("https://boinc.com/myproject")
        == "BOINC.COM/MYPROJECT"
    )
    assert (
        main.resolve_url_database("http://boinc.com/myproject") == "BOINC.COM/MYPROJECT"
    )


def test_resolve_url_list_to_database():
    url_list = ["https://www.boinc.com/myproject", "http://boinc.com/myproject"]
    assert main.resolve_url_list_to_database(url_list) == [
        "BOINC.COM/MYPROJECT",
        "BOINC.COM/MYPROJECT",
    ]


def test_temp_check():
    # test it only activates when temp control enabled
    main.ENABLE_TEMP_CONTROL = False
    assert main.temp_check()
    # make sure it turns on and off at correct setpoints
    main.ENABLE_TEMP_CONTROL = True
    main.TEMP_COMMAND = "echo 67"
    main.START_TEMP = 66
    main.STOP_TEMP = 70
    assert main.temp_check()
    main.TEMP_COMMAND = "echo 77"
    assert not main.temp_check()


# Tests that require a network connection to work. Should be run sparingly for this reason
def test_update_fetch():
    actual_version = main.VERSION
    actual_update_check = main.DATABASE.get("LASTUPDATECHECK")
    update_text = """## Format: Version, SecurityBool (1 or 0), Notes
    ## UPDATE FILE FOR FINDTHEMAG DO NOT DELETE THIS LINE
    1.0,0,Original Version
    2.0,0,Main version
    2.1,0,Update is strongly suggested fixes several major bugs in project handling
    2.2,1,FindTheMag critical security update please see Github for more info
    2.3,0,Various usability improvements and crash fixes
    """
    # assert it finds updates incl security updates
    main.DATABASE["LASTUPDATECHECK"] = datetime.datetime(1997, 3, 3)
    update, security, text = main.update_fetch(update_text, 0.1)
    assert update
    assert security
    assert text
    # assert no false positives
    main.DATABASE["LASTUPDATECHECK"] = datetime.datetime(1997, 3, 3)
    update, security, text = main.update_fetch(update_text, 1000)
    assert not update
    assert not security
    assert not text
    # assert correctly identifying security updates
    main.DATABASE["LASTUPDATECHECK"] = datetime.datetime(1997, 3, 3)
    update, security, text = main.update_fetch(update_text, 2.2)
    assert update
    assert not security
    assert text
    # assert not checking too often
    main.DATABASE["LASTUPDATECHECK"] = datetime.datetime.now()
    update, security, text = main.update_fetch(update_text, 0.1)
    assert not update
    assert not security
    assert not text
    # reset original variables
    main.VERSION = actual_version
    if actual_update_check:
        main.DATABASE["LASTUPDATECHECK"] = actual_update_check


def test_get_grc_price():
    sample_text = """CMC               }</script></div><script id="__NEXT_DATA__" type="application/json">{"props":{"initialI18nStore":{"en":{"common":{"Open App":"Open"},"coin-detail-page":{"Please wait, we are loading chart data ":"Please wait a moment. ","More news on the way, please stay tuned...":"More news updates are on the way... Stay tuned!","***Significantly differs from the cryptocurrency's price; excluded from the overall price and\n            volume calculation":"***Significantly differs from the cryptocurrency's price; excluded from the overall price and volume calculation","The CMC team has not verified the project's Market Cap. However, according to the project, its self-reported CS is {{selfReportedCirculatingSupply}} {{symbol}} with a self-reported market cap of {{selfReportedMarketCap}}.":"CoinMarketCap has not verified the project's market cap. However, according to the project, its self-reported circulating supply is {{selfReportedCirculatingSupply}} {{symbol}} with a self-reported market cap of {{selfReportedMarketCap}}.","coin_detail_wallets_seo_text":"\u003ch2 id='what-are-cryptocurrency-wallets-'\u003eWhat Are Cryptocurrency Wallets?\u003c/h2\u003e \u003cp\u003eCryptocurrency \u003ca href='https://coinmarketcap.com/alexandria/glossary/wallet'\u003ewallets\u003c/a\u003e are software programs that store private and public keys and interface with various blockchain to enable users to send and receive digital currency and monitor their balance. It is the equivalent of a bank account where you can both deposit and withdraw funds from (though only the latter with cryptocurrency).\u003c/p\u003e \u003cp\u003eCryptocurrency wallets store private and public keys and facilitate the sending and receiving of digital currency and monitor all transactions to protect from identity theft. The private key is used to authorize payments, while the public key is used to access received funds.\u003c/p\u003e \u003cp\u003eCryptocurrency wallets can be hot, meaning that they are connected to the internet, or cold, meaning that they have no internet connection. When deciding whether to use a \u003ca href='https://coinmarketcap.com/alexandria/article/hot-wallets-vs-cold-wallets-whats-the-difference'\u003ehot wallet vs a cold wallet\u003c/a\u003e, you need to consider several factors: while hot wallets are often more user friendly, they also carry a higher risk of loss of funds due to their internet connection.\u003c/p\u003e \u003ch2 id='what-are-the-main-types-of-cryptocurrency-wallets-'\u003eWhat Are the Main Types of Cryptocurrency Wallets?\u003c/h2\u003e \u003ch3 id='-paper-wallets-https-coinmarketcap-com-alexandria-glossary-paper-wallet-'\u003e\u003ca href='https://coinmarketcap.com/alexandria/glossary/paper-wallet'\u003ePaper Wallets\u003c/a\u003e\u003c/h3\u003e \u003cp\u003eCryptocurrency paper wallets are a secure way to hold your cryptocurrencies. Think of them like a savings account with no withdrawal limits. A paper wallet contains both the public and private key for your wallet. The wallet can be used to receive cryptocurrencies from other people. It is also possible to send cryptocurrency to this address if it is generated with a genuine random number generator (RNG).\u003c/p\u003e \u003cp\u003eThey are simple, secure and offline alternatives to digital cryptocurrency wallets. They have all of the benefits of paper money while also providing the unique ability to securely cold-store digital currency without any possibility of a hacker or malware gaining access to your funds.\u003c/p\u003e \u003ch3 id='-hot-wallets-https-coinmarketcap-com-alexandria-glossary-hot-wallet-'\u003e\u003ca href='https://coinmarketcap.com/alexandria/glossary/hot-wallet'\u003eHot Wallets\u003c/a\u003e\u003c/h3\u003e \u003cp\u003eCryptocurrency hot wallets are also known as web wallets or online wallets.These types of wallets are used to make small, frequent payments while requiring the least amount of effort from the individual and/or organization. \u003c/p\u003e \u003cp\u003eCryptocurrency hot wallets are a digital wallet used to store cryptocurrency funds. A hot wallet is an online system and can be accessed from anywhere as it does not require any physical access to the unit. For example, \u003ca href='https://coinmarketcap.com/exchanges/coinbase-pro/'\u003eCoinbase\u003c/a\u003e is a popular exchange platform for buying cryptocurrency in the U.S. and Europe, but they also have a web-based digital wallet which allows users to store \u003ca href='https://coinmarketcap.com/currencies/bitcoin/'\u003eBitcoin\u003c/a\u003e, \u003ca href='https://coinmarketcap.com/currencies/litecoin/'\u003eLitecoin\u003c/a\u003e and \u003ca href='https://coinmarketcap.com/currencies/ethereum'\u003eEther\u003c/a\u003e, among other coins.\u003c/p\u003e \u003cp\u003e\u003ca href='https://coinmarketcap.com/alexandria/article/what-is-metamask'\u003eMetaMask\u003c/a\u003e is another popular hot wallet.\u003c/p\u003e \u003ch3 id='-cold-wallets-https-coinmarketcap-com-alexandria-glossary-cold-wallet-'\u003e\u003ca href='https://coinmarketcap.com/alexandria/glossary/cold-wallet'\u003eCold Wallets\u003c/a\u003e\u003c/h3\u003e \u003cp\u003eCold wallets refer to any method of storing cryptocurrency which keeps the private keys of your coins offline, preventing any form of hacking, stealing, or unauthorized access. Paper wallets and other cold wallets are considered to be more secure as compared to hot storage solutions such as online and software wallets, which make transactions much easier but are often less secure due to security issues.\u003c/p\u003e \u003ch3 id='how-to-use-a-bitcoin-wallet'\u003eHow to Use a Bitcoin Wallet\u003c/h3\u003e \u003cp\u003eCoinMarketCap Alexandria has a guide that teaches you \u003ca href='https://coinmarketcap.com/alexandria/article/how-to-use-a-bitcoin-wallet'\u003ehow to use a Bitcoin wallet here\u003c/a\u003e.\u003c/p\u003e","Ends ":"Ends in ","Starts ":"Starts in ","All Pairs":"All pairs","Show Less":"Hide","Log in to track your portfolio":"Log in to track portfolio","Log in to keep your watchlist when you’re on a different device or you remove cookies.":"Log in to keep your watchlist on different devices or when removing cookies.","Max 20 items are allowed in the local watchlist":"Max. 20 items allowed in a local watchlist.","Ratio showing investment potential of a cryptocurrency.\u003c1\u003e\u003c/1\u003e\u003c1\u003e\u003c/1\u003eIf value \u003e 1, the cryptocurrency tends to be overvalued.\u003c1\u003e\u003c/1\u003eIf value \u003c 0, the cryptocurrency tends to be undervalued.":"Ratio showing investment potential of a cryptocurrency.\u003c1\u003e\u003c1\u003eIf value \u003e 1, the cryptocurrency tends to be overvalued.\u003c1\u003eIf value \u003c 0, the cryptocurrency tends to be undervalued.","Market Cap = Current price x Circulating supply.":"Market cap = Current price x Circulating supply","The amount of coins that have been already created, minus any coins that have been burned (if there were any). It is analogous to the outstanding shares in the stock market.":"Total supply = Total coins created - coins that have been burned (if any) It is comparable to outstanding shares in the stock market.","If this data has not been submitted by the project or verified by the CMC team, total supply shows --.":"If the project did not submit this data nor was it verified by CoinMarketCap, total supply shows “--”.","If this data has not been submitted by the project or verified by the CMC team, max supply shows --.":"If the project did not submit this data nor was it verified by CoinMarketCap, max. supply shows \"--\".","Self reported Circulating supply":"Self-reported circulating supply","Track in your portfolio":"Track in portfolio","Show all members":"Show all"},"gravity-post":{},"community-editor":{},"gravity":{},"portfolio":{},"sheet_Dexer":{"dexscan_toplatest_block_web":"Latest block","dexscan_pairstartooltip_web":"Add pair to watchlist","dexscan_toplatest_blocktime_web":"{{count}}s ago","dexscan_pooledpercent_web":"% Pooled {{coin}}","cdp_h1_web":"{{coin_name}} \u003c1\u003eprice\u003c/1\u003e","dexscan_pdptotalliquidity_web":"Total liquidity","dexscan_pdptotalliquiditytooltip_web":"The ability of both assets to be sold or exchanged quickly without affecting its prices.","dexscan_pdpvolume24h_web":"Volume (24h)","dexscan_pdpvolume24htooltip_web":"A measure of how much a pair was traded in this pool in the last 24 hours.","dexscan_pdpholders_web":"Holders","dexscan_pdpholderstooltip_web":"The number of unique wallet addresses that contain a non-zero balance of this pair.","dexscan_pdpvolumequotecoin_web":"Volume {{quote coin}} (24h)","dexscan_pdpvolumequotecointooltip_web":"A measure of how much {{quote coin}} was traded in this pool in the last 24 hours.","dexscan_pdppooledbasecoin_web":"Pooled {{base coin}}","dexscan_pdppooledbasecointooltip_web":"The amount of {{base coin}} liquidity in this pool.","dexscan_pdppooledquotecoin_web":"Pooled {{quote coin}}","dexscan_pdppooledquotecointooltip_web":"The amount of {{quote coin}} liquidity in this pool.","dexscan_pdp%pooledbasecoin_web":"% Pooled {{base coin}}","dexscan_pdp%pooledbasecointooltip_web":"The percentage of {{base coin}} in this pool vs. total supply.","dexscan_pdppoolcreated_web":"Pool created","dexscan_pdppoolcreatedtooltip_web":"The time this pool was deployed on this DEX.","dexscan_pdpbuytax_web":"Buy tax","dexscan_pdpbuytaxtooltip_web":"The amount of tax incurred when buying this token.","dexscan_pdpselltax_web":"Sell tax","dexscan_pdpselltaxtooltip_web":"The amount of tax incurred when selling this token.","The amount of coins that have been already created, minus any coins that have been burned (if there were any). It is analogous to the outstanding shares in the stock market.":"Total supply = Total coins created - coins that have been burned (if any) It is comparable to outstanding shares in the stock market.","If this data has not been submitted by the project or verified by the CMC team, total supply shows --.":"If the project did not submit this data nor was it verified by CoinMarketCap, total supply shows “--”.","Fully Diluted Value: (Total Supply-Burned Supply)*Price{{v1}}":"Fully Diluted Value: (Total Supply - Burned Supply)*Price","dexscan_goplus_contraveriftooltip_web":"This token has an open source contract and details can be retrieved from the contract code.","dexscan_goplus_honeypottooltip_web":"This token potentially cannot be sold due to the token’s contract function; or the token contains malicious code.","dexscan_converter_web":"{{name}} to {{name2}} converter","dexscan_telegrambot_desc_web":"Get real-time notifications on Telegram by adding this bot","dexscan_tokenholders_web":"Token holders","dexscan_top10holders_web":"Top 10 holders ratio","dexscan_ownershold_web":"Owner's holdings","dexscan_creatorshold_web":"Creator's holdings","dexscan_goplus_disclaim1_web":"All information and data relating to contract detection are based on public third party information. CoinMarketCap does not confirm or verify the accuracy or timeliness of such information and data.","dexscan_goplus_disclaim2_web":"CoinMarketCap shall have no responsibility or liability for the accuracy of data, nor have the duty to review, confirm, verify or otherwise perform any inquiry or investigation as to the completeness, accuracy, sufficiency, integrity, reliability or timeliness of any such information or data provided."}}},"initialLanguage":"en","i18nServerInstance":null,"pageProps":{"detailRes":{"detail":{"id":833,"name":"Gridcoin","symbol":"GRC","slug":"gridcoin","category":"coin","description":"Gridcoin (GRC) is a cryptocurrency . Gridcoin has a current supply of 459,186,751.23683 with 428,533,719.08864963 in circulation. The last known price of Gridcoin is 0.00997987 USD and is down -1.64 over the last 24 hours. It is currently trading on 4 active market(s) with $38,780.09 traded over the last 24 hours. More information can be found at http://www.gridcoin.us/.","dateAdded":"2015-02-28T00:00:00.000Z","status":"active","notice":"","alertType":2,"alertLink":"","latestUpdateTime":"2023-07-16T01:09:00.000Z","watchCount":"2341","watchListRanking":4280,"launchPrice":0.00226245,"tags":[{"slug":"pos","name":"PoS","category":"ALGORITHM"},{"slug":"sha-256","name":"SHA-256","category":"ALGORITHM"}],"urls":{"website":["http://www.gridcoin.us/"],"technical_doc":["https://www.gridcoin.us/assets/img/whitepaper.pdf"],"explorer":["https://gridcoin.network/","https://gridcoinstats.eu/block"],"source_code":["https://github.com/gridcoin-community/Gridcoin-Research"],"message_board":["https://coinmarketcap.com/community/search/top/gridcoin","https://cryptocurrencytalk.com/forum/464-gridcoin-grc/"],"chat":["https://t.me/gridcoin","https://discord.gg/Bt4YHxJ"],"announcement":["https://bitcointalk.org/index.php?topic=324118.0"],"reddit":["https://reddit.com/r/gridcoin"],"facebook":[],"twitter":["https://twitter.com/GridcoinNetwork"]},"volume":38756.57629286,"volumeChangePercentage24h":1.9136,"cexVolume":38756.57629286,"dexVolume":0,"statistics":{"price":0.009984916033862508,"priceChangePercentage1h":0.29985299,"priceChangePercentage24h":-1.52179387,"priceChangePercentage7d":-7.23077964,"priceChangePercentage30d":-8.71132797,"priceChangePercentage60d":-18.01154491,"priceChangePercentage90d":-49.5560064,"priceChangePercentageAll":4.41331997880711,"marketCap":4278873.2,"marketCapChangePercentage24h":-1.516,"fullyDilutedMarketCap":4584941.15,"fullyDilutedMarketCapChangePercentage24h":-1.52,"circulatingSupply":428533719.08864963,"totalSupply":459186751.23683,"marketCapDominance":0.0004,"rank":989,"roi":341.33200883,"low24h":0.009707191796260024,"high24h":0.010030531194002316,"low7d":0.009707191796260024,"high7d":0.012635256822792975,"low30d":0.009280060511602744,"high30d":0.012635256822792975,"low90d":0.009280060511602744,"high90d":0.019677672240814806,"low52w":0.003935920040293885,"high52w":0.02411719622262274,"lowAllTime":0.000458133989013732,"highAllTime":0.2112410068511963,"lowAllTimeChangePercentage":2079.48,"highAllTimeChangePercentage":-95.27,"lowAllTimeTimestamp":"2015-04-25T23:04:25.000Z","highAllTimeTimestamp":"2018-01-09T12:54:03.000Z","lowYesterday":0.009707191796260024,"highYesterday":0.010182758377397693,"openYesterday":0.010182758377397693,"closeYesterday":0.009952106724349314,"priceChangePercentageYesterday":-2.27,"volumeYesterday":39120.41,"turnover":0.00905766,"ytdPriceChangePercentage":28.582,"volumeRank":2766,"volumeMcRank":3431,"mcTotalNum":10156,"volumeTotalNum":10156,"volumeMcTotalNum":10156,"status":""},"relatedCoins":[{"id":2513,"name":"GoldMint","slug":"goldmint","price":0.08533020686889306,"priceChangePercentage24h":0.07684376,"priceChangePercentage7d":0.82150525},{"id":4679,"name":"Band Protocol","slug":"band-protocol","price":1.2446745015957559,"priceChangePercentage24h":1.02747429,"priceChangePercentage7d":2.27566552},{"id":7083,"name":"Uniswap","slug":"uniswap","price":5.800180822200075,"priceChangePercentage24h":-0.4278961,"priceChangePercentage7d":9.35067113},{"id":1414,"name":"Firo","slug":"firo","price":1.7262244621909546,"priceChangePercentage24h":-1.29119085,"priceChangePercentage7d":-0.88906589},{"id":1975,"name":"Chainlink","slug":"chainlink","price":6.878880716695128,"priceChangePercentage24h":-0.17576128,"priceChangePercentage7d":10.42279198},{"id":7653,"name":"Oasis Network","slug":"oasis-network","price":0.05145675161395962,"priceChangePercentage24h":0.1907189,"priceChangePercentage7d":6.96735553},{"id":707,"name":"Blocknet","slug":"blocknet","price":0.07914566371533448,"priceChangePercentage24h":-1.48518129,"priceChangePercentage7d":5.95481716},{"id":5864,"name":"yearn.finance","slug":"yearn-finance","price":7039.903543206167,"priceChangePercentage24h":0.54353635,"priceChangePercentage7d":-1.76382121},{"id":4279,"name":"Solar","slug":"sxp","price":0.37509250910469943,"priceChangePercentage24h":1.21997494,"priceChangePercentage7d":-3.84024832},{"id":8043,"name":"MahaDAO","slug":"mahadao","price":0.36291590267352297,"priceChangePercentage24h":0.10161449,"priceChangePercentage7d":-9.81422062}],"relatedExchanges":[{"id":562,"name":"Txbit","slug":"txbit"},{"id":121,"name":"SouthXchange","slug":"southxchange"}],"isAudited":false,"holders":{},"displayTV":1,"isInfiniteMaxSupply":0,"tvCoinSymbol":"GRC","useFaq":true,"faqDescription":[{"q":"","a":"Gridcoin (GRC) is a cryptocurrency . Gridcoin has a current supply of 459,186,751.23683 with 428,533,719.08864963 in circulation. The last known price of Gridcoin is 0.00997987 USD and is down -1.64 over the last 24 hours. It is currently trading on 4 active market(s) with $38,780.09 traded over the last 24 hours. More information can be found at http://www.gridcoin.us/.","isQ":false}],"holdersFlag":false,"ratingsFlag":false,"analysisFlag":false,"socialsFlag":true,"cryptoRating":[],"selfReportedTags":[],"dateLaunched":"","platforms":[]},"article":[],"trending":{"trendingList":[{"id":52,"dataType":2,"name":"XRP","symbol":"XRP","slug":"xrp","rank":5,"status":"active","marketCap":37934906657.48,"selfReportedMarketCap":0,"priceChange":{"price":0.7219633120276707,"priceChange24h":2.87550878,"priceChange7d":53.14228566,"priceChange30d":51.42858738,"volume24h":3137737468.635285,"lastUpdate":"2023-07-16T01:09:00.000Z"}},{"id":24478,"dataType":2,"name":"Pepe","symbol":"PEPE","slug":"pepe","rank":66,"status":"active","marketCap":649348669.56,"selfReportedMarketCap":697247228.8686819,"priceChange":{"price":0.0000016573895953521165,"priceChange24h":2.03417944,"priceChange7d":5.41637257,"priceChange30d":84.86004595,"volume24h":106847945.11669448,"lastUpdate":"2023-07-16T01:09:00.000Z"}},{"id":22153,"dataType":2,"name":"ELF Wallet","symbol":"ELF","slug":"elf-wallet","rank":2659,"status":"active","marketCap":0,"selfReportedMarketCap":247741.30832466652,"priceChange":{"price":0.0004374086319294456,"priceChange24h":-48.85888252,"priceChange7d":63.2855435,"priceChange30d":-96.94931562,"volume24h":2889029.95907961,"lastUpdate":"2023-07-16T01:09:00.000Z"}},{"id":512,"dataType":2,"name":"Stellar","symbol":"XLM","slug":"stellar","rank":23,"status":"active","marketCap":3491217261.71,"selfReportedMarketCap":0,"priceChange":{"price":0.12864445153489226,"priceChange24h":-2.6579174,"priceChange7d":29.27962766,"priceChange30d":68.63602224,"volume24h":179752636.4116227,"lastUpdate":"2023-07-16T01:09:00.000Z"}},{"id":1,"dataType":2,"name":"Bitcoin","symbol":"BTC","slug":"bitcoin","rank":1,"status":"active","marketCap":589104591771.67,"selfReportedMarketCap":0,"priceChange":{"price":30318.765639655598,"priceChange24h":-0.00962614,"priceChange7d":-0.20552637,"priceChange30d":19.1254255,"volume24h":7719004725.713283,"lastUpdate":"2023-07-16T01:09:00.000Z"}}]},"gravityFlag":true,"projectInfoFlag":true,"airDropFlag":false,"hasOngoingAirdrop":false,"announcement":[],"mainAccount":{"nickname":"CoinMarketCap","handle":"CoinMarketCap","avatarId":"621c22097aafe46422aa1161","createdTime":"1639224157447","type":2,"status":0,"biography":"The world's most trusted cryptocurrency data authority","originalBiography":"[[{\"type\":\"text\",\"content\":\"The world's most trusted cryptocurrency data authority\"}]]","currencies":[],"birthDate":"1368025200000","websiteLink":"https://linktr.ee/CoinMarketCapOfficial","authType":1,"announceType":0,"lastUpdateAvatarId":"1684382465199","avatar":{"url":"https://s3.coinmarketcap.com/static-gravity/image/2d30e95978a74a6a969341470b4f1327.jpeg","status":2},"biographyAuditStatus":2,"preBiography":"","preOriginalBiography":"","preTopics":[],"preCurrencies":[],"vip":false,"banner":{"url":"https://s3.coinmarketcap.com/static-gravity/image/14df023dfac84173ab4e68e2103d2526.jpeg","status":2,"originalBannerUrl":"https://s3.coinmarketcap.com/static-gravity/image/f9148e67e2a6468f8714bcb8bc09b2dd.jpeg"},"isMainProject":false,"guid":"24013915"},"announcementNew":[]},"namespacesRequired":["common","coin-detail-page","gravity-post","community-editor","gravity","portfolio","sheet_Dexer"],"reqLanguage":"en","useRemakePage":true,"userABGroupString":"navBar-B_featureLab-A_revampThemis-A","reqLang":"en","globalMetrics":{"numCryptocurrencies":26324,"numMarkets":63007,"activeExchanges":644,"marketCap":1216276091520.7107,"marketCapChange":0.245997,"totalVol":26536766964.85,"stablecoinVol":23187952838.662827,"stablecoinChange":-51.763424313024,"totalVolChange":-50.651131,"defiVol":2556695461.2595468,"defiChange":-42.346577719472,"defiMarketCap":46781552832.53868,"derivativesVol":125020884134.59924,"derivativeChange":-56.894226525829,"btcDominance":48.424083268765,"btcDominanceChange":-0.136396141235,"ethDominance":19.120417844198,"etherscanGas":{"lastBlock":"17702484","slowPrice":"12","slowConfirmationTime":"45","standardPrice":"12","standardConfirmationTime":"45","fastPrice":"12","fastConfirmationTime":"45"}},"dailyVideos":[{"url":"https://www.youtube.com/watch?v=W6VBf9qD35A","date":"2022-07-09T00:00:00.000Z"}],"pageSharedData":{"topCategories":[{"title":" 🔥 FTX Bankruptcy Estate","relatedTagSlug":"ftx-bankruptcy-estate"},{"title":" 🔥 Alleged SEC Securities","relatedTagSlug":"alleged-sec-securities"},{"title":" 🔥 Liquid Staking Derivatives","relatedTagSlug":"liquid-staking-derivatives"},{"title":" 🔥 DeFi","relatedTagSlug":"defi"}],"fearGreedIndexData":{"currentIndex":{"score":57.9549259695917,"maxScore":100,"name":"Neutral","updateTime":"2023-07-16T00:00:00.000Z"},"dialConfig":[{"start":0,"end":20,"name":"Extreme fear"},{"start":20,"end":40,"name":"Fear"},{"start":40,"end":60,"name":"Neutral"},{"start":60,"end":80,"name":"Greed"},{"start":80,"end":100,"name":"Extreme greed"}]},"deviceInfo":{"isDesktop":true,"isTablet":false,"isMobile":false}},"pageSize":100,"noindex":false},"theme":"DAY","getInitialStart":1689469979149,"getInitialEnd":1689469979161,"dehydratedState":{"mutations":[],"queries":[{"state":{"data":{"numCryptocurrencies":26324,"numMarkets":63007,"activeExchanges":644,"marketCap":1216276091520.7107,"marketCapChange":0.245997,"totalVol":26536766964.85,"stablecoinVol":23187952838.662827,"stablecoinChange":-51.763424313024,"totalVolChange":-50.651131,"defiVol":2556695461.2595468,"defiChange":-42.346577719472,"defiMarketCap":46781552832.53868,"derivativesVol":125020884134.59924,"derivativeChange":-56.894226525829,"btcDominance":48.424083268765,"btcDominanceChange":-0.136396141235,"ethDominance":19.120417844198,"etherscanGas":{"lastBlock":"17702484","slowPrice":"12","slowConfirmationTime":"45","standardPrice":"12","standardConfirmationTime":"45","fastPrice":"12","fastConfirmationTime":"45"}},"dataUpdateCount":1,"dataUpdatedAt":1689469979161,"error":null,"errorUpdateCount":0,"errorUpdatedAt":0,"fetchFailureCount":0,"fetchMeta":null,"isFetching":false,"isInvalidated":false,"isPaused":false,"status":"success"},"queryKey":["global-metric"],"queryHash":"[\"global-metric\"]"}]},"userABGroup":"navBar-B_featureLab-A_revampThemis-A","quotesLatestData":[{"id":9022,"symbol":"SATS","p":0.00030322903720363104,"p1h":0.06466128,"p24h":-0.00070701,"p7d":-0.26602745,"p30d":19.14301434,"p60d":11.93317862,"p90d":1.3692883,"t":1689469800000},{"id":9023,"symbol":"BITS","p":0.0303229037203631,"p1h":0.06466128,"p24h":-0.00070701,"p7d":-0.26602745,"p30d":19.14301434,"p60d":11.93317862,"p90d":1.3692883,"t":1689469800000},{"id":1,"symbol":"BTC","p":30322.9037203631,"p1h":0.06466128,"p24h":-0.00070701,"p7d":-0.26602745,"p30d":19.14301434,"p60d":11.93317862,"p90d":1.3692883,"t":1689469800000},{"id":1027,"symbol":"ETH","p":1935.5011885099855,"p1h":0.13168257,"p24h":0.26129864,"p7d":3.31878249,"p30d":16.5439595,"p60d":5.9977619,"p90d":-7.33615112,"t":1689469800000},{"id":2781,"symbol":"USD","p":1,"p1h":0,"p24h":0,"p7d":0,"p30d":0,"p60d":0,"p90d":0,"t":1689469743000}],"initialState":"{\"app\":{\"locale\":\"en-US\",\"theme\":\"DAY\",\"lang\":\"en\",\"country\":\"\",\"currency\":{\"id\":2781,\"name\":\"United States Dollar\",\"symbol\":\"usd\",\"token\":\"$\"},\"bottomBannerHeights\":{},\"browser\":{},\"window\":{\"width\":0,\"height\":0,\"isNarrowLayout\":false},\"modal\":{\"instance\":0,\"data\":{}},\"message\":\"\",\"isInApp\":false},\"cryptocurrency\":{\"listingLatest\":{\"page\":1,\"sort\":\"rank\",\"sortDirection\":\"asc\",\"data\":[],\"filters\":{},\"totalItems\":0},\"ItemKeyMap\":{},\"quoteKey\":[],\"listingHistorical\":{\"data\":[],\"page\":1,\"sort\":\"\",\"sortDirection\":\"\"},\"new\":{\"page\":1,\"sort\":\"\",\"sortDirection\":\"\",\"data\":[]},\"watchlist\":{\"page\":1,\"sort\":\"\",\"sortDirection\":\"\",\"data\":[]},\"map\":{\"data\":[],\"slugMap\":{}},\"info\":{},\"prices\":{},\"quotesLatest\":{},\"quotesHistorical\":{\"loading\":true},\"ohlcvHistorical\":{},\"marketPairsLatest\":{\"data\":{}},\"pricePerformanceStatsLatest\":{\"data\":{}},\"topDerivatives\":[],\"yieldFarmingRankingLatest\":{\"filterKey\":\"\"},\"gainersLosers\":{\"gainers\":[],\"losers\":[],\"sortGainers\":\"\",\"sortDirectionGainers\":\"\",\"sortLosers\":\"\",\"sortDirectionLosers\":\"\"},\"trendingCoins\":{\"sort\":\"\",\"sortDirection\":\"\",\"data\":[]},\"mostViewed\":{\"sort\":\"\",\"sortDirection\":\"\",\"data\":[]},\"spotlight\":{\"data\":{}},\"gravityRecommend\":{\"data\":{}},\"dexpairSearch\":[]},\"exchange\":{\"map\":{\"data\":[]},\"info\":{},\"quotesLatest\":{},\"marketPairsLatest\":{\"data\":{}},\"fiatOnRamp\":{\"activeSection\":null,\"selectedCrypto\":null,\"availableCurrencies\":[\"USD\",\"EUR\",\"GBP\",\"NGN\",\"RUB\"],\"selectedCurrency\":\"USD\",\"orderBy\":\"price\",\"order\":\"asc\",\"tableData\":[]}},\"globalMetrics\":{\"quotesHistorical\":{},\"trendingSearch\":[],\"categoriesList\":[]},\"watchlist\":{\"loaded\":false,\"data\":[],\"onboarding\":[],\"import\":null,\"counts\":{\"isLoading\":false,\"data\":{}}},\"user\":{\"data\":null,\"isLoading\":false,\"isLoaded\":true,\"loginModal\":\"\",\"loginContinue\":null},\"notification\":[],\"sponsoredAds\":{}}"},"page":"/currencies/[...cryptocurrencySlug]","query":{"cryptocurrencySlug":["gridcoin"]},"buildId":"9zr3BWvGAZewNzOGJTv7J","assetPrefix":"https://s2.coinmarketcap.com","runtimeConfig":{"localeSubpaths":{"ar":"ar","bg":"bg","cs":"cs","da":"da","de":"de","el":"el","es":"es","fi":"fi","fr":"fr","hi":"hi","hu":"hu","id":"id","it":"it","ja":"ja","ko":"ko","nl":"nl","no":"no","pl":"pl","pt-br":"pt-br","ro":"ro","ru":"ru","sk":"sk","sv":"sv","th":"th","tr":"tr","uk":"uk","ur":"ur","vi":"vi","zh-tw":"zh-tw","zh":"zh"}},"isFallback":false,"dynamicIds":[90960,67652],"customServer":true,"gip":true,"appGip":true,"scriptLoader":[]}</script><script>
YAHOO  </div></div></div></div></div></div></div><div class="Cl(b)"></div></div></div></div></div></div><script>if (window.performance) {window.performance.mark && window.performance.mark('Lead-2-FinanceHeader');window.performance.measure && window.performance.measure('Lead-2-FinanceHeaderDone','PageStart','Lead-2-FinanceHeader');}</script></div><div><div id="mrt-node-Lead-3-FeatureBar" data-locator="subtree-root"><div id="Lead-3-FeatureBar-Proxy" data-reactroot=""></div></div><script>if (window.performance) {window.performance.mark && window.performance.mark('Lead-3-FeatureBar');window.performance.measure && window.performance.measure('Lead-3-FeatureBarDone','PageStart','Lead-3-FeatureBar');}</script></div><div><div id="mrt-node-Lead-4-DcmPixelIFrame" data-locator="subtree-root"><div id="Lead-4-DcmPixelIFrame-Proxy" data-reactroot=""><iframe id="quote-dcm-pixel-iframe" src="https://s.yimg.com/jk/gtm/gtm_ns.html?id=GTM-K85MQ6N&amp;cat=wlistclk&amp;u1=5bbf5264b1c55a306d943761aaef09cf3338b5df061480bd142c151e75ba41cc" class="H(1px) W(1px) Bd(0) D(n)"></iframe></div></div><script>if (window.performance) {window.performance.mark && window.performance.mark('Lead-4-DcmPixelIFrame');window.performance.measure && window.performance.measure('Lead-4-DcmPixelIFrameDone','PageStart','Lead-4-DcmPixelIFrame');}</script></div><div><div id="mrt-node-Lead-5-QuoteHeader" data-locator="subtree-root"><div id="Lead-5-QuoteHeader-Proxy" data-reactroot=""><div id="quote-header-info" data-yaft-module="tdv2-applet-QuoteHeader" class="quote-header-section Cf Pos(r) Mb(5px) Bgc($lv2BgColor) Maw($maxModuleWidth) Miw($minGridWidth) smartphone_Miw(ini) Miw(ini)!--tab768 Miw(ini)!--tab1024 Mstart(a) Mend(a) Px(20px) smartphone_Pb(0px) smartphone_Mb(0px) smartphone_Z(11)" data-test="quote-header"><div class="W(100%) Bdts(s) Bdtw(7px)  Bdtc($negativeColor)"></div><div class="Mt(15px) D(f) Pos(r)"><div class="D(ib) Mt(-5px) Maw(38%)--tab768 Maw(38%) Mend(10px) Ov(h) smartphone_Maw(85%) smartphone_Mend(0px)"><div class="D(ib) "><h1 class="D(ib) Fz(18px)">Gridcoin USD (GRC-USD)</h1></div><div class="C($tertiaryColor) Fz(12px)"><span>CCC  - CoinMarketCap. Currency in USD</span></div></div><div class="followButton Cur(p) Fz(14px) smartphone_Fz(12px) smartphone_Mt(8px) Mend(8px) Pos(r)" data-test="dropdown"><div class="Pos(r) D(ib) Cur(p)" tabindex="0" title="Follow" role="button" aria-label="Follow"><div class="addButton C(white) Bgc($linkSelectedColor) Bgc($linkSelectedHoverColor):h Bdrs(30px) Px(16px) Py(6px)"><svg class="Stk(white) Fill(white) Va(tb)! Cur(p)" width="16" style="stroke-width:0;vertical-align:bottom" height="16" viewBox="0 0 24 24" data-icon="star"><path d="M8.485 7.83l-6.515.21c-.887.028-1.3 1.117-.66 1.732l4.99 4.78-1.414 6.124c-.2 1.14.767 1.49 1.262 1.254l5.87-3.22 5.788 3.22c.48.228 1.464-.097 1.26-1.254l-1.33-6.124 4.962-4.78c.642-.615.228-1.704-.658-1.732l-6.486-.21-2.618-6.22c-.347-.815-1.496-.813-1.84.003L8.486 7.83zm7.06 6.05l1.11 5.11-4.63-2.576L7.33 18.99l1.177-5.103-4.088-3.91 5.41-.18 2.19-5.216 2.19 5.216 5.395.18-4.06 3.903z"></path></svg><span class="Mx(5px) Fw(600) Va(m)"><span>Follow</span></span></div></div></div><div class="D(ib) Va(t) Fx(a) Mend(8px)"><a class="pageViewLink D(ib) Td(n) Pstart(15px) Pend(12px) Py(6px) Fz(12px) Fw(500) C($tertiaryColor) Bd Bdc($seperatorColor) Bdrs(15px) Bgc($linkColor):h Bgc($linkColor):f C(white):h C(white):f Bdc($linkColor):h Bdc($linkColor):f" href="/chart/GRC-USD?studies=Visitor%20Trend&amp;ncid=dcm_306158729_490172245_127172993" data-test="visitor-trend-link"><svg class="Mend(8px) Fill($linkColor) Stk($linkColor) pageViewLink:h_Stk(white)! pageViewLink:h_Fill(white)! Va(m)! Cur(p)" width="16" style="stroke-width:0;vertical-align:bottom" height="16" viewBox="0 0 48 48" data-icon="groups"><path d="M14.4 12c-2.206 0-4 1.794-4 4s1.794 4 4 4 4-1.794 4-4-1.794-4-4-4m0 12c-4.412 0-8-3.588-8-8s3.588-8 8-8 8 3.588 8 8-3.588 8-8 8zM34 12c-2.206 0-4 1.794-4 4s1.794 4 4 4 4-1.794 4-4-1.794-4-4-4zm0 12c-4.412 0-8-3.588-8-8s3.588-8 8-8 8 3.588 8 8-3.588 8-8 8zm-9.948 12H5.756v-1.336c0-1.196 2.22-4.662 9.024-4.664 6.024 0 9.272 2.402 9.272 4.664V36zM14.87 26C5.992 26.002 2 31.068 2 34.664V40h26v-5.336C28 30.49 23.894 26 14.87 26zM47 34.664C47 30.49 43.052 26 34.378 26c-3.27 0-5.652.738-7.378 1.652 1.058.966 1.86 2.058 2.394 3.216C30.61 30.37 32.23 30 34.382 30c5.792 0 8.914 2.402 8.914 4.664V36H30.242v4H47v-5.336z"></path></svg><span class="Mend(8px) Va(m) D(ib) D(n)--sm3"><span>Visitors trend</span></span><span class="D(ib) Va(m) Mend(8px)"><span>2W</span><svg class="pageViewLink:h_Stk(white) pageViewLink:h_Fill(white) Fill($negativeColor) Stk($negativeColor) Va(t)! Cur(p)" width="16" style="stroke-width:0;vertical-align:bottom" height="16" viewBox="0 0 48 48" data-icon="arrow-down"><path d="M34.7 29.5c.793-.773.81-2.038.04-2.83-.77-.79-2.037-.81-2.83-.038l-5.677 5.525V8.567h-4v23.59l-5.68-5.525c-.79-.77-2.058-.753-2.827.04-.378.388-.566.89-.566 1.394 0 .52.202 1.042.605 1.434l10.472 10.183L34.7 29.5z"></path></svg></span><span class="D(ib) Va(m) Mend(8px)"><span>10W</span><svg class="pageViewLink:h_Stk(white) pageViewLink:h_Fill(white) Fill($positiveColor) Stk($positiveColor) Va(t)! Cur(p)" width="16" style="stroke-width:0;vertical-align:bottom" height="16" viewBox="0 0 48 48" data-icon="arrow-up"><path d="M13.764 18.75c-.792.772-.808 2.037-.04 2.828.772.792 2.038.81 2.83.04l5.678-5.526v23.59h4v-23.59l5.68 5.525c.79.77 2.058.753 2.827-.04.377-.388.565-.89.565-1.394 0-.52-.202-1.042-.605-1.434L24.23 8.566 13.763 18.75z"></path></svg></span><span class="D(ib) Va(m)"><span>9M</span><svg class="pageViewLink:h_Stk(white) pageViewLink:h_Fill(white) Fill($positiveColor) Stk($positiveColor) Va(t)! Cur(p)" width="16" style="stroke-width:0;vertical-align:bottom" height="16" viewBox="0 0 48 48" data-icon="arrow-up"><path d="M13.764 18.75c-.792.772-.808 2.037-.04 2.828.772.792 2.038.81 2.83.04l5.678-5.526v23.59h4v-23.59l5.68 5.525c.79.77 2.058.753 2.827-.04.377-.388.565-.89.565-1.394 0-.52-.202-1.042-.605-1.434L24.23 8.566 13.763 18.75z"></path></svg></span></a></div><div class="D(ib) Fl(end) W(20%) Maw(300px) Mstart(a) Cl(end)--mobxl W(250px)--tab768 "><div class="Pos(r) D(ib) Mend(10px) Va(m) W(100%) O(n):f O(n):h" data-id="fin-quote-lookup" data-yaft-module="tdv2-applet-SymbolLookup"><form data-finsrch="quote" class="Pos(r)"><input type="text" aria-autocomplete="both" autoCapitalize="off" autoComplete="false" autoCorrect="false" class="D(ib) Pstart(10px) Bxz(bb) Bgc($lv3BgColor) W(100%) H(32px) Lh(32px) Bdrs(0) Bxsh(n) Fz(s) Bg(n) Bd O(n):f O(n):h Bdc($seperatorColor) Bdc($linkColor):f finsrch-inpt" placeholder="Quote Lookup"/><button class="End(1px) H(32px) Lh(n) Va(m) Pos(a) Fl(end) Bdrs(2px) Td(n) Fz(s) D(ib) Bxz(bb) Px(10px) Bd Bgc($linkColor) Bgc($linkActiveColor):h finsrch-btn" aria-label="Search" type="submit"><svg class="Fill(white) Stk(white) Va(m)! Cur(p)" width="20" style="stroke-width:0;vertical-align:bottom" height="20" viewBox="0 0 24 24" data-icon="search"><path d="M9 3C5.686 3 3 5.686 3 9c0 3.313 2.686 6 6 6s6-2.687 6-6c0-3.314-2.686-6-6-6m13.713 19.713c-.387.388-1.016.388-1.404 0l-7.404-7.404C12.55 16.364 10.85 17 9 17c-4.418 0-8-3.582-8-8 0-4.42 3.582-8 8-8s8 3.58 8 8c0 1.85-.634 3.55-1.69 4.905l7.403 7.404c.39.386.39 1.015 0 1.403"></path></svg></button><div class="W(100%) Bxz(bb) finsrch-rslt finsrch-show-ftr"></div></form></div></div></div><div class="My(6px) Pos(r) smartphone_Mt(6px) W(100%) D(ib) smartphone_Mb(10px) W(100%)--mobp"><div class="D(ib) Va(m) Maw(65%) Ov(h)"><div class="D(ib) Mend(20px)"><fin-streamer class="Fw(b) Fz(36px) Mb(-4px) D(ib)" data-symbol="GRC-USD" data-test="qsp-price" data-field="regularMarketPrice" data-trend="none" data-pricehint="6" value="0.010000787" active="">0.010001</fin-streamer><fin-streamer class="Fw(500) Pstart(8px) Fz(24px)" data-symbol="GRC-USD" data-test="qsp-price-change" data-field="regularMarketChange" data-trend="txt" data-pricehint="6" value="-0.00013607834" active=""><span class="C($negativeColor)">-0.000136</span></fin-streamer> <fin-streamer class="Fw(500) Pstart(8px) Fz(24px)" data-symbol="GRC-USD" data-field="regularMarketChangePercent" data-trend="txt" data-pricehint="6" data-template="({fmt})" value="-0.013424115" active=""><span class="C($negativeColor)">(-1.34%)</span></fin-streamer><fin-streamer class="D(n)" data-symbol="GRC-USD" changeev="regularTimeChange" data-field="regularMarketTime" data-trend="none" value="" active="true"></fin-streamer><fin-streamer class="D(n)" data-symbol="GRC-USD" changeev="marketState" data-field="marketState" data-trend="none" value="" active="true"></fin-streamer><div id="quote-market-notice" class="C($tertiaryColor) D(b) Fz(12px) Fw(n) Mstart(0)--mobpsm Mt(6px)--mobpsm Whs(n)"><span>As of  01:17AM UTC. Market open.</span></div></div></div><div class="Pos(r) Z(1) D(ib) Mstart(30px) Va(t) uba-container"><div id="defaultTRADENOW-sizer" class="uba-container D-n D(n)"><div id="defaultTRADENOW-wrapper" class=""><div id="defaultdestTRADENOW" class="D(ib)" style=""> <div class='D(f) Jc(c) Ai(c) Ta(c) Bgc(#f5f8fa) H(100%) W(100%)'> <i class='Fz(12px) C(#6e7780) Fs(n) Mx(a)'>
COINGECKO <span class="tw-text-gray-900 dark:tw-text-white tw-text-3xl"><span class="no-wrap" data-price-btc="0.000000359918670050423" data-coin-id="243" data-coin-symbol="grc" data-target="price.price">$0.010917170129</span></span>   """
    price = main.get_grc_price(sample_text)
    print("price is {}".format(price))
    assert price == 0.010208382975086675


def test_get_approved_project_urls_web():
    original_gs_resolver_dict = main.DATABASE.get("GSRESOLVERDICT")
    original_last_check = main.DATABASE.get("LASTGRIDCOINSTATSPROJECTCHECK")
    # verify it returns cache if recently requested
    main.DATABASE["GSRESOLVERDICT"] = True
    main.DATABASE["LASTGRIDCOINSTATSPROJECTCHECK"] = datetime.datetime.now()
    a = main.get_approved_project_urls_web()
    assert a
    # reset to original values
    if original_gs_resolver_dict:
        main.DATABASE["GSRESOLVERDICT"] = original_gs_resolver_dict
    else:
        del main.DATABASE["GSRESOLVERDICT"]
    if original_last_check:
        main.DATABASE["LASTGRIDCOINSTATSPROJECTCHECK"] = original_last_check
    else:
        del main.DATABASE["LASTGRIDCOINSTATSPROJECTCHECK"]
    # verify we get the expected output
    query_result = """{"Amicable_Numbers":{"version":2,"display_name":"Amicable Numbers","url":"https:\/\/sech.me\/boinc\/Amicable\/@","base_url":"https:\/\/sech.me\/boinc\/Amicable\/","display_url":"https:\/\/sech.me\/boinc\/Amicable\/","stats_url":"https:\/\/sech.me\/boinc\/Amicable\/stats\/","gdpr_controls":false,"time":"2023-07-14 10:58:32 UTC"},"asteroids@home":{"version":2,"display_name":"asteroids@home","url":"https:\/\/asteroidsathome.net\/boinc\/@","base_url":"https:\/\/asteroidsathome.net\/boinc\/","display_url":"https:\/\/asteroidsathome.net\/boinc\/","stats_url":"https:\/\/asteroidsathome.net\/boinc\/stats\/","gdpr_controls":false,"time":"2023-07-14 11:01:32 UTC"},"einstein@home":{"version":2,"display_name":"einstein@home","url":"https:\/\/einstein.phys.uwm.edu\/@","base_url":"https:\/\/einstein.phys.uwm.edu\/","display_url":"https:\/\/einstein.phys.uwm.edu\/","stats_url":"https:\/\/einstein.phys.uwm.edu\/stats\/","gdpr_controls":true,"time":"2023-07-14 11:04:33 UTC"},"folding@home":{"version":2,"display_name":"folding@home","url":"https:\/\/foldingathome.div72.xyz\/@","base_url":"https:\/\/foldingathome.div72.xyz\/","display_url":"https:\/\/foldingathome.div72.xyz\/","stats_url":"https:\/\/foldingathome.div72.xyz\/stats\/","gdpr_controls":false,"time":"2023-07-14 11:07:33 UTC"},"milkyway@home":{"version":2,"display_name":"milkyway@home","url":"https:\/\/milkyway.cs.rpi.edu\/milkyway\/@","base_url":"https:\/\/milkyway.cs.rpi.edu\/milkyway\/","display_url":"https:\/\/milkyway.cs.rpi.edu\/milkyway\/","stats_url":"https:\/\/milkyway.cs.rpi.edu\/milkyway\/stats\/","gdpr_controls":false,"time":"2023-07-14 11:10:33 UTC"},"nfs@home":{"version":2,"display_name":"nfs@home","url":"https:\/\/escatter11.fullerton.edu\/nfs\/@","base_url":"https:\/\/escatter11.fullerton.edu\/nfs\/","display_url":"https:\/\/escatter11.fullerton.edu\/nfs\/","stats_url":"https:\/\/escatter11.fullerton.edu\/nfs\/stats\/","gdpr_controls":false,"time":"2023-07-14 11:13:34 UTC"},"numberfields@home":{"version":2,"display_name":"numberfields@home","url":"https:\/\/numberfields.asu.edu\/NumberFields\/@","base_url":"https:\/\/numberfields.asu.edu\/NumberFields\/","display_url":"https:\/\/numberfields.asu.edu\/NumberFields\/","stats_url":"https:\/\/numberfields.asu.edu\/NumberFields\/stats\/","gdpr_controls":true,"time":"2023-07-14 11:16:34 UTC"},"odlk1":{"version":2,"display_name":"odlk1","url":"https:\/\/boinc.multi-pool.info\/latinsquares\/@","base_url":"https:\/\/boinc.multi-pool.info\/latinsquares\/","display_url":"https:\/\/boinc.multi-pool.info\/latinsquares\/","stats_url":"https:\/\/boinc.multi-pool.info\/latinsquares\/stats\/","gdpr_controls":false,"time":"2023-07-14 11:19:35 UTC"},"rosetta@home":{"version":2,"display_name":"rosetta@home","url":"https:\/\/boinc.bakerlab.org\/rosetta\/@","base_url":"https:\/\/boinc.bakerlab.org\/rosetta\/","display_url":"https:\/\/boinc.bakerlab.org\/rosetta\/","stats_url":"https:\/\/boinc.bakerlab.org\/rosetta\/stats\/","gdpr_controls":false,"time":"2023-07-14 11:22:35 UTC"},"SiDock@home":{"version":2,"display_name":"SiDock@home","url":"https:\/\/www.sidock.si\/sidock\/@","base_url":"https:\/\/www.sidock.si\/sidock\/","display_url":"https:\/\/www.sidock.si\/sidock\/","stats_url":"https:\/\/www.sidock.si\/sidock\/stats\/","gdpr_controls":false,"time":"2023-07-14 11:25:35 UTC"},"SRBase":{"version":2,"display_name":"SRBase","url":"https:\/\/srbase.my-firewall.org\/sr5\/@","base_url":"https:\/\/srbase.my-firewall.org\/sr5\/","display_url":"https:\/\/srbase.my-firewall.org\/sr5\/","stats_url":"https:\/\/srbase.my-firewall.org\/sr5\/stats\/","gdpr_controls":false,"time":"2023-07-14 11:28:36 UTC"},"TN-Grid":{"version":2,"display_name":"TN-Grid","url":"https:\/\/gene.disi.unitn.it\/test\/@","base_url":"https:\/\/gene.disi.unitn.it\/test\/","display_url":"https:\/\/gene.disi.unitn.it\/test\/","stats_url":"https:\/\/gene.disi.unitn.it\/test\/stats\/","gdpr_controls":false,"time":"2023-07-14 11:31:36 UTC"},"universe@home":{"version":2,"display_name":"universe@home","url":"https:\/\/universeathome.pl\/universe\/@","base_url":"https:\/\/universeathome.pl\/universe\/","display_url":"https:\/\/universeathome.pl\/universe\/","stats_url":"https:\/\/universeathome.pl\/universe\/stats\/","gdpr_controls":true,"time":"2023-07-14 11:34:36 UTC"},"World_Community_Grid":{"version":2,"display_name":"World Community Grid","url":"https:\/\/www.worldcommunitygrid.org\/boinc\/@","base_url":"https:\/\/www.worldcommunitygrid.org\/boinc\/","display_url":"https:\/\/www.worldcommunitygrid.org\/","stats_url":"https:\/\/www.worldcommunitygrid.org\/boinc\/stats\/","gdpr_controls":true,"time":"2023-07-14 11:37:37 UTC"},"yoyo@home":{"version":2,"display_name":"yoyo@home","url":"https:\/\/www.rechenkraft.net\/yoyo\/@","base_url":"https:\/\/www.rechenkraft.net\/yoyo\/","display_url":"https:\/\/www.rechenkraft.net\/yoyo\/","stats_url":"https:\/\/www.rechenkraft.net\/yoyo\/stats\/","gdpr_controls":false,"time":"2023-07-14 11:40:37 UTC"}}"""
    answer = main.get_approved_project_urls_web(query_result)
    assert isinstance(answer, dict)
    assert len(answer) > 3
    assert "Amicable_Numbers" in answer
    assert answer.get("Amicable_Numbers") == "SECH.ME/BOINC/AMICABLE"


def test_xfers_happening():
    # test xfer list w stalled xfers
    xfer_list = [{"status": 0, "persistent_file_xfer": {"num_retries": 2}}]
    assert not main.xfers_happening(xfer_list)
    # test empty xfer list
    xfer_list = []
    assert not main.xfers_happening(xfer_list)
    # test xfer list w xfers happening
    xfer_list = [
        {
            "status": 0,
        }
    ]
    assert main.xfers_happening(xfer_list)


def test_get_gridcoin_config_parameters():
    result = main.get_gridcoin_config_parameters(".")
    assert result.get("enablesidestaking") == "1"
    assert isinstance(result.get("sidestake"), list)
    assert "bc3NA8e8E3EoTL1qhRmeprbjWcmuoZ26A2,1" in result.get("sidestake", [])
    assert "RzUgcntbFm8PeSJpauk6a44qbtu92dpw3K,1" in result.get("sidestake", [])
    assert result["rpcport"] == "9876"
    assert result["rpcuser"] == "myusername"
    assert result["rpcpassword"] == "mypassword"


def test_check_sidestake():
    # check it notices when sidestaking disabled
    config = {
        "enablesidestaking": "0",
        "sidestake": [
            "bc3NA8e8E3EoTL1qhRmeprbjWcmuoZ26A2,1",
            "RzUgcntbFm8PeSJpauk6a44qbtu92dpw3K,1",
        ],
        "rpcport": "9876",
        "rpcallowip": "127.0.0.1",
        "server": "1",
        "rpcuser": "myusername",
        "rpcpassword": "mypassword",
    }
    assert not main.check_sidestake(config, "bc3NA8e8E3EoTL1qhRmeprbjWcmuoZ26A2", 1)
    # check it notices if value too low
    config = {
        "enablesidestaking": "1",
        "sidestake": [
            "bc3NA8e8E3EoTL1qhRmeprbjWcmuoZ26A2,1",
            "RzUgcntbFm8PeSJpauk6a44qbtu92dpw3K,1",
        ],
        "rpcport": "9876",
        "rpcallowip": "127.0.0.1",
        "server": "1",
        "rpcuser": "myusername",
        "rpcpassword": "mypassword",
    }
    assert not main.check_sidestake(config, "bc3NA8e8E3EoTL1qhRmeprbjWcmuoZ26A2", 5)
    # assert it correctly detects sidestake
    config = {
        "enablesidestaking": "1",
        "sidestake": [
            "bc3NA8e8E3EoTL1qhRmeprbjWcmuoZ26A2,1",
            "RzUgcntbFm8PeSJpauk6a44qbtu92dpw3K,1",
        ],
        "rpcport": "9876",
        "rpcallowip": "127.0.0.1",
        "server": "1",
        "rpcuser": "myusername",
        "rpcpassword": "mypassword",
    }
    assert main.check_sidestake(config, "bc3NA8e8E3EoTL1qhRmeprbjWcmuoZ26A2", 1)


def test_project_url_from_stats_file():
    assert (
        main.project_url_from_stats_file("job_log_www.worldcommunitygrid.org.txt")
        == "WORLDCOMMUNITYGRID.ORG"
    )
    assert (
        main.project_url_from_stats_file("job_log_escatter11.fullerton.edu_nfs.txt")
        == "ESCATTER11.FULLERTON.EDU/NFS"
    )
    assert (
        main.project_url_from_stats_file("job_log_www.rechenkraft.net_yoyo.txt")
        == "RECHENKRAFT.NET/YOYO"
    )


def test_project_url_from_credit_history_file():
    assert (
        main.project_url_from_credit_history_file(
            "statistics_boinc.multi-pool.info_latinsquares.xml"
        )
        == "BOINC.MULTI-POOL.INFO/LATINSQUARES"
    )
    assert (
        main.project_url_from_credit_history_file(
            "statistics_boinc.bakerlab.org_rosetta.xml"
        )
        == "BOINC.BAKERLAB.ORG/ROSETTA"
    )
    assert (
        main.project_url_from_credit_history_file(
            "statistics_milkyway.cs.rpi.edu_milkyway.xml"
        )
        == "MILKYWAY.CS.RPI.EDU/MILKYWAY"
    )


def test_stat_file_to_list():
    example = """1680334251 ue 4017.278236 ct 3454.260000 fe 200000000000000 nm TASK1 et 3465.445294 es 0
1680334604 ue 4017.278236 ct 3805.396000 fe 200000000000000 nm TASK2 et 3819.634777 es 0
1680336346 ue 2381.072619 ct 2074.329000 fe 70000000000000 nm TASK3 et 2094.352010 es 0
1680337549 ue 3190.839339 ct 2930.237000 fe 70000000000000 nm TASK4 et 2944.508444 es 0"""
    result = main.stat_file_to_list(None, example)
    assert result == [
        {
            "STARTTIME": "1680334251",
            "ESTTIME": "4017.278236",
            "CPUTIME": "3454.260000",
            "ESTIMATEDFLOPS": "200000000000000",
            "TASKNAME": "TASK1",
            "WALLTIME": "3465.445294",
            "EXITCODE": "0",
        },
        {
            "STARTTIME": "1680334604",
            "ESTTIME": "4017.278236",
            "CPUTIME": "3805.396000",
            "ESTIMATEDFLOPS": "200000000000000",
            "TASKNAME": "TASK2",
            "WALLTIME": "3819.634777",
            "EXITCODE": "0",
        },
        {
            "STARTTIME": "1680336346",
            "ESTTIME": "2381.072619",
            "CPUTIME": "2074.329000",
            "ESTIMATEDFLOPS": "70000000000000",
            "TASKNAME": "TASK3",
            "WALLTIME": "2094.352010",
            "EXITCODE": "0",
        },
        {
            "STARTTIME": "1680337549",
            "ESTTIME": "3190.839339",
            "CPUTIME": "2930.237000",
            "ESTIMATEDFLOPS": "70000000000000",
            "TASKNAME": "TASK4",
            "WALLTIME": "2944.508444",
            "EXITCODE": "0",
        },
    ]


def test_calculate_credit_averages():
    my_input = {
        "WORLDCOMMUNITYGRID.ORG": {
            "CREDIT_HISTORY": {"04-07-2023": {"CREDITAWARDED": 0.0}},
            "WU_HISTORY": {
                "04-09-2023": {
                    "TOTALWUS": 1,
                    "total_wall_time": 9084.946866,
                    "total_cpu_time": 9072.151,
                },
                "04-10-2023": {
                    "TOTALWUS": 3,
                    "total_wall_time": 41053.747675,
                    "total_cpu_time": 41004.234,
                },
            },
            "COMPILED_STATS": {},
        },
        "SECH.ME/BOINC/AMICABLE": {
            "CREDIT_HISTORY": {"03-31-2023": {"CREDITAWARDED": 0.0}},
            "WU_HISTORY": {
                "01-22-2023": {
                    "TOTALWUS": 3,
                    "total_wall_time": 51544.448429,
                    "total_cpu_time": 102921.05000000002,
                }
            },
            "COMPILED_STATS": {},
        },
        "ESCATTER11.FULLERTON.EDU/NFS": {
            "CREDIT_HISTORY": {"03-31-2023": {"CREDITAWARDED": 0.0}},
            "WU_HISTORY": {
                "04-01-2023": {
                    "TOTALWUS": 4,
                    "total_wall_time": 12323.940525000002,
                    "total_cpu_time": 12264.222000000002,
                }
            },
            "COMPILED_STATS": {},
        },
        "RECHENKRAFT.NET/YOYO": {
            "CREDIT_HISTORY": {},
            "WU_HISTORY": {
                "10-02-2022": {
                    "TOTALWUS": 1,
                    "total_wall_time": 6818.480898,
                    "total_cpu_time": 19051.76,
                }
            },
            "COMPILED_STATS": {},
        },
        "BOINC.BAKERLAB.ORG/ROSETTA": {
            "CREDIT_HISTORY": {"04-07-2023": {"CREDITAWARDED": 0.0}},
            "WU_HISTORY": {},
            "COMPILED_STATS": {},
        },
    }
    result = main.calculate_credit_averages(my_input)
    assert result == {
        "WORLDCOMMUNITYGRID.ORG": {
            "TOTALCREDIT": 0.0,
            "AVGWALLTIME": 3.481853787569444,
            "AVGCPUTIME": 3.477526736111111,
            "AVGCREDITPERTASK": 0.0,
            "TOTALTASKS": 4,
            "TOTALWALLTIME": 13.927415150277776,
            "TOTALCPUTIME": 13.910106944444443,
            "AVGCREDITPERHOUR": 0.0,
            "XDAYWALLTIME": 0.0,
        },
        "SECH.ME/BOINC/AMICABLE": {
            "TOTALCREDIT": 0.0,
            "AVGWALLTIME": 4.772634113796296,
            "AVGCPUTIME": 9.529726851851853,
            "AVGCREDITPERTASK": 0.0,
            "TOTALTASKS": 3,
            "TOTALWALLTIME": 14.317902341388889,
            "TOTALCPUTIME": 28.58918055555556,
            "AVGCREDITPERHOUR": 0.0,
            "XDAYWALLTIME": 0.0,
        },
        "ESCATTER11.FULLERTON.EDU/NFS": {
            "TOTALCREDIT": 0.0,
            "AVGWALLTIME": 0.8558292031250001,
            "AVGCPUTIME": 0.8516820833333334,
            "AVGCREDITPERTASK": 0.0,
            "TOTALTASKS": 4,
            "TOTALWALLTIME": 3.4233168125000004,
            "TOTALCPUTIME": 3.4067283333333336,
            "AVGCREDITPERHOUR": 0.0,
            "XDAYWALLTIME": 0.0,
        },
        "RECHENKRAFT.NET/YOYO": {
            "TOTALCREDIT": 0,
            "AVGWALLTIME": 1.8940224716666665,
            "AVGCPUTIME": 5.292155555555555,
            "AVGCREDITPERTASK": 0.0,
            "TOTALTASKS": 1,
            "TOTALWALLTIME": 1.8940224716666665,
            "TOTALCPUTIME": 5.292155555555555,
            "AVGCREDITPERHOUR": 0.0,
            "XDAYWALLTIME": 0.0,
        },
        "BOINC.BAKERLAB.ORG/ROSETTA": {
            "TOTALCREDIT": 0.0,
            "AVGWALLTIME": 0,
            "AVGCPUTIME": 0,
            "AVGCREDITPERTASK": 0,
            "TOTALTASKS": 0,
            "TOTALWALLTIME": 0,
            "TOTALCPUTIME": 0,
            "AVGCREDITPERHOUR": 0,
            "XDAYWALLTIME": 0,
        },
    }


def test_config_files_to_stats():
    assert main.config_files_to_stats("/path/that/doesntexist") == {}
    result = main.config_files_to_stats("boinc_stats")
    expected = {
        "WORLDCOMMUNITYGRID.ORG": {
            "CREDIT_HISTORY": {"04-07-2023": {"CREDITAWARDED": 0.0}},
            "WU_HISTORY": {
                "04-09-2023": {
                    "TOTALWUS": 1,
                    "total_wall_time": 9084.946866,
                    "total_cpu_time": 9072.151,
                },
                "04-10-2023": {
                    "TOTALWUS": 3,
                    "total_wall_time": 41053.747675,
                    "total_cpu_time": 41004.234,
                },
            },
            "COMPILED_STATS": {
                "TOTALCREDIT": 0.0,
                "AVGWALLTIME": 3.481853787569444,
                "AVGCPUTIME": 3.477526736111111,
                "AVGCREDITPERTASK": 0.0,
                "TOTALTASKS": 4,
                "TOTALWALLTIME": 13.927415150277776,
                "TOTALCPUTIME": 13.910106944444443,
                "AVGCREDITPERHOUR": 0.0,
                "XDAYWALLTIME": 0.0,
            },
        },
        "SECH.ME/BOINC/AMICABLE": {
            "CREDIT_HISTORY": {"03-31-2023": {"CREDITAWARDED": 0.0}},
            "WU_HISTORY": {
                "01-22-2023": {
                    "TOTALWUS": 3,
                    "total_wall_time": 51544.448429,
                    "total_cpu_time": 102921.05000000002,
                }
            },
            "COMPILED_STATS": {
                "TOTALCREDIT": 0.0,
                "AVGWALLTIME": 4.772634113796296,
                "AVGCPUTIME": 9.529726851851853,
                "AVGCREDITPERTASK": 0.0,
                "TOTALTASKS": 3,
                "TOTALWALLTIME": 14.317902341388889,
                "TOTALCPUTIME": 28.58918055555556,
                "AVGCREDITPERHOUR": 0.0,
                "XDAYWALLTIME": 0.0,
            },
        },
        "ESCATTER11.FULLERTON.EDU/NFS": {
            "CREDIT_HISTORY": {"03-31-2023": {"CREDITAWARDED": 0.0}},
            "WU_HISTORY": {
                "04-01-2023": {
                    "TOTALWUS": 4,
                    "total_wall_time": 12323.940525000002,
                    "total_cpu_time": 12264.222000000002,
                }
            },
            "COMPILED_STATS": {
                "TOTALCREDIT": 0.0,
                "AVGWALLTIME": 0.8558292031250001,
                "AVGCPUTIME": 0.8516820833333334,
                "AVGCREDITPERTASK": 0.0,
                "TOTALTASKS": 4,
                "TOTALWALLTIME": 3.4233168125000004,
                "TOTALCPUTIME": 3.4067283333333336,
                "AVGCREDITPERHOUR": 0.0,
                "XDAYWALLTIME": 0.0,
            },
        },
        "RECHENKRAFT.NET/YOYO": {
            "CREDIT_HISTORY": {},
            "WU_HISTORY": {
                "10-02-2022": {
                    "TOTALWUS": 1,
                    "total_wall_time": 6818.480898,
                    "total_cpu_time": 19051.76,
                }
            },
            "COMPILED_STATS": {
                "TOTALCREDIT": 0,
                "AVGWALLTIME": 1.8940224716666665,
                "AVGCPUTIME": 5.292155555555555,
                "AVGCREDITPERTASK": 0.0,
                "TOTALTASKS": 1,
                "TOTALWALLTIME": 1.8940224716666665,
                "TOTALCPUTIME": 5.292155555555555,
                "AVGCREDITPERHOUR": 0.0,
                "XDAYWALLTIME": 0.0,
            },
        },
        "BOINC.BAKERLAB.ORG/ROSETTA": {
            "CREDIT_HISTORY": {"04-07-2023": {"CREDITAWARDED": 0.0}},
            "WU_HISTORY": {},
            "COMPILED_STATS": {
                "TOTALCREDIT": 0.0,
                "AVGWALLTIME": 0,
                "AVGCPUTIME": 0,
                "AVGCREDITPERTASK": 0,
                "TOTALTASKS": 0,
                "TOTALWALLTIME": 0,
                "TOTALCPUTIME": 0,
                "AVGCREDITPERHOUR": 0,
                "XDAYWALLTIME": 0,
            },
        },
    }
    assert frozenset(result) == frozenset(expected)


def test_add_mag_to_combined_stats():
    expected = {}
    result = {}
    combined_stats = main.config_files_to_stats("boinc_stats_2")
    example_ratios = {
        "WORLDCOMMUNITYGRID.ORG": 0.01,
        "SECH.ME/BOINC/AMICABLE": 0.99,
        "ESCATTER11.FULLERTON.EDU/NFS": 0.0,
    }
    approved_projects = list(example_ratios.keys())
    approved_projects.remove(
        "ESCATTER11.FULLERTON.EDU/NFS"
    )  # test it gives zero mag for unapproved project
    return1, return2 = main.add_mag_to_combined_stats(
        combined_stats, example_ratios, approved_projects, preferred_projects=[]
    )
    expected_return_1 = {
        "WORLDCOMMUNITYGRID.ORG": {
            "CREDIT_HISTORY": {"06-15-2023": {"CREDITAWARDED": 349.815304}},
            "WU_HISTORY": {
                "04-09-2023": {
                    "TOTALWUS": 1,
                    "total_wall_time": 9084.946866,
                    "total_cpu_time": 9072.151,
                },
                "04-10-2023": {
                    "TOTALWUS": 3,
                    "total_wall_time": 41053.747675,
                    "total_cpu_time": 41004.234,
                },
            },
            "COMPILED_STATS": {
                "TOTALCREDIT": 349.815304,
                "AVGWALLTIME": 3.481853787569444,
                "AVGCPUTIME": 3.477526736111111,
                "AVGCREDITPERTASK": 87.453826,
                "TOTALTASKS": 4,
                "TOTALWALLTIME": 13.927415150277776,
                "TOTALCPUTIME": 13.910106944444443,
                "AVGCREDITPERHOUR": 25.11702998908761,
                "XDAYWALLTIME": 0.0,
                "AVGMAGPERHOUR": 0.2511702998908761,
                "MAGPERCREDIT": 0.01,
            },
        },
        "SECH.ME/BOINC/AMICABLE": {
            "CREDIT_HISTORY": {"06-15-2023": {"CREDITAWARDED": 0.0}},
            "WU_HISTORY": {
                "01-22-2023": {
                    "TOTALWUS": 3,
                    "total_wall_time": 51544.448429,
                    "total_cpu_time": 102921.05000000002,
                }
            },
            "COMPILED_STATS": {
                "TOTALCREDIT": 0.0,
                "AVGWALLTIME": 4.772634113796296,
                "AVGCPUTIME": 9.529726851851853,
                "AVGCREDITPERTASK": 0.0,
                "TOTALTASKS": 3,
                "TOTALWALLTIME": 14.317902341388889,
                "TOTALCPUTIME": 28.58918055555556,
                "AVGCREDITPERHOUR": 0.0,
                "XDAYWALLTIME": 0.0,
                "AVGMAGPERHOUR": 0.0,
                "MAGPERCREDIT": 0.99,
            },
        },
        "ESCATTER11.FULLERTON.EDU/NFS": {
            "CREDIT_HISTORY": {"06-15-2023": {"CREDITAWARDED": 0.0}},
            "WU_HISTORY": {
                "04-01-2023": {
                    "TOTALWUS": 4,
                    "total_wall_time": 12323.940525000002,
                    "total_cpu_time": 12264.222000000002,
                }
            },
            "COMPILED_STATS": {
                "TOTALCREDIT": 0.0,
                "AVGWALLTIME": 0.8558292031250001,
                "AVGCPUTIME": 0.8516820833333334,
                "AVGCREDITPERTASK": 0.0,
                "TOTALTASKS": 4,
                "TOTALWALLTIME": 3.4233168125000004,
                "TOTALCPUTIME": 3.4067283333333336,
                "AVGCREDITPERHOUR": 0.0,
                "XDAYWALLTIME": 0.0,
                "AVGMAGPERHOUR": 0,
                "MAGPERCREDIT": 0,
            },
        },
        "RECHENKRAFT.NET/YOYO": {
            "CREDIT_HISTORY": {"06-15-2023": {"CREDITAWARDED": 0.0}},
            "WU_HISTORY": {
                "10-02-2022": {
                    "TOTALWUS": 1,
                    "total_wall_time": 6818.480898,
                    "total_cpu_time": 19051.76,
                }
            },
            "COMPILED_STATS": {
                "TOTALCREDIT": 0.0,
                "AVGWALLTIME": 1.8940224716666665,
                "AVGCPUTIME": 5.292155555555555,
                "AVGCREDITPERTASK": 0.0,
                "TOTALTASKS": 1,
                "TOTALWALLTIME": 1.8940224716666665,
                "TOTALCPUTIME": 5.292155555555555,
                "AVGCREDITPERHOUR": 0.0,
                "XDAYWALLTIME": 0.0,
                "AVGMAGPERHOUR": 0,
                "MAGPERCREDIT": 0,
            },
        },
        "BOINC.MULTI-POOL.INFO/LATINSQUARES": {
            "CREDIT_HISTORY": {"06-15-2023": {"CREDITAWARDED": 0.0}},
            "WU_HISTORY": {},
            "COMPILED_STATS": {
                "TOTALCREDIT": 0.0,
                "AVGWALLTIME": 0,
                "AVGCPUTIME": 0,
                "AVGCREDITPERTASK": 0,
                "TOTALTASKS": 0,
                "TOTALWALLTIME": 0,
                "TOTALCPUTIME": 0,
                "AVGCREDITPERHOUR": 0,
                "XDAYWALLTIME": 0,
                "AVGMAGPERHOUR": 0,
                "MAGPERCREDIT": 0,
            },
        },
        "BOINC.BAKERLAB.ORG/ROSETTA": {
            "CREDIT_HISTORY": {"06-15-2023": {"CREDITAWARDED": 0.0}},
            "WU_HISTORY": {},
            "COMPILED_STATS": {
                "TOTALCREDIT": 0.0,
                "AVGWALLTIME": 0,
                "AVGCPUTIME": 0,
                "AVGCREDITPERTASK": 0,
                "TOTALTASKS": 0,
                "TOTALWALLTIME": 0,
                "TOTALCPUTIME": 0,
                "AVGCREDITPERHOUR": 0,
                "XDAYWALLTIME": 0,
                "AVGMAGPERHOUR": 0,
                "MAGPERCREDIT": 0,
            },
        },
        "UNIVERSEATHOME.PL/UNIVERSE": {
            "CREDIT_HISTORY": {"06-15-2023": {"CREDITAWARDED": 0.0}},
            "WU_HISTORY": {},
            "COMPILED_STATS": {
                "TOTALCREDIT": 0.0,
                "AVGWALLTIME": 0,
                "AVGCPUTIME": 0,
                "AVGCREDITPERTASK": 0,
                "TOTALTASKS": 0,
                "TOTALWALLTIME": 0,
                "TOTALCPUTIME": 0,
                "AVGCREDITPERHOUR": 0,
                "XDAYWALLTIME": 0,
                "AVGMAGPERHOUR": 0,
                "MAGPERCREDIT": 0,
            },
        },
        "MILKYWAY.CS.RPI.EDU/MILKYWAY": {
            "CREDIT_HISTORY": {"06-15-2023": {"CREDITAWARDED": 0.0}},
            "WU_HISTORY": {},
            "COMPILED_STATS": {
                "TOTALCREDIT": 0.0,
                "AVGWALLTIME": 0,
                "AVGCPUTIME": 0,
                "AVGCREDITPERTASK": 0,
                "TOTALTASKS": 0,
                "TOTALWALLTIME": 0,
                "TOTALCPUTIME": 0,
                "AVGCREDITPERHOUR": 0,
                "XDAYWALLTIME": 0,
                "AVGMAGPERHOUR": 0,
                "MAGPERCREDIT": 0,
            },
        },
        "EINSTEIN.PHYS.UWM.EDU": {
            "CREDIT_HISTORY": {"06-15-2023": {"CREDITAWARDED": 0.0}},
            "WU_HISTORY": {},
            "COMPILED_STATS": {
                "TOTALCREDIT": 0.0,
                "AVGWALLTIME": 0,
                "AVGCPUTIME": 0,
                "AVGCREDITPERTASK": 0,
                "TOTALTASKS": 0,
                "TOTALWALLTIME": 0,
                "TOTALCPUTIME": 0,
                "AVGCREDITPERHOUR": 0,
                "XDAYWALLTIME": 0,
                "AVGMAGPERHOUR": 0,
                "MAGPERCREDIT": 0,
            },
        },
        "SRBASE.MY-FIREWALL.ORG/SR5": {
            "CREDIT_HISTORY": {"06-15-2023": {"CREDITAWARDED": 0.0}},
            "WU_HISTORY": {},
            "COMPILED_STATS": {
                "TOTALCREDIT": 0.0,
                "AVGWALLTIME": 0,
                "AVGCPUTIME": 0,
                "AVGCREDITPERTASK": 0,
                "TOTALTASKS": 0,
                "TOTALWALLTIME": 0,
                "TOTALCPUTIME": 0,
                "AVGCREDITPERHOUR": 0,
                "XDAYWALLTIME": 0,
                "AVGMAGPERHOUR": 0,
                "MAGPERCREDIT": 0,
            },
        },
        "GPUGRID.NET": {
            "CREDIT_HISTORY": {"06-15-2023": {"CREDITAWARDED": 0.0}},
            "WU_HISTORY": {},
            "COMPILED_STATS": {
                "TOTALCREDIT": 0.0,
                "AVGWALLTIME": 0,
                "AVGCPUTIME": 0,
                "AVGCREDITPERTASK": 0,
                "TOTALTASKS": 0,
                "TOTALWALLTIME": 0,
                "TOTALCPUTIME": 0,
                "AVGCREDITPERHOUR": 0,
                "XDAYWALLTIME": 0,
                "AVGMAGPERHOUR": 0,
                "MAGPERCREDIT": 0,
            },
        },
        "GENE.DISI.UNITN.IT/TEST": {
            "CREDIT_HISTORY": {"06-15-2023": {"CREDITAWARDED": 0.0}},
            "WU_HISTORY": {},
            "COMPILED_STATS": {
                "TOTALCREDIT": 0.0,
                "AVGWALLTIME": 0,
                "AVGCPUTIME": 0,
                "AVGCREDITPERTASK": 0,
                "TOTALTASKS": 0,
                "TOTALWALLTIME": 0,
                "TOTALCPUTIME": 0,
                "AVGCREDITPERHOUR": 0,
                "XDAYWALLTIME": 0,
                "AVGMAGPERHOUR": 0,
                "MAGPERCREDIT": 0,
            },
        },
        "SIDOCK.SI/SIDOCK": {
            "CREDIT_HISTORY": {"06-15-2023": {"CREDITAWARDED": 0.0}},
            "WU_HISTORY": {},
            "COMPILED_STATS": {
                "TOTALCREDIT": 0.0,
                "AVGWALLTIME": 0,
                "AVGCPUTIME": 0,
                "AVGCREDITPERTASK": 0,
                "TOTALTASKS": 0,
                "TOTALWALLTIME": 0,
                "TOTALCPUTIME": 0,
                "AVGCREDITPERHOUR": 0,
                "XDAYWALLTIME": 0,
                "AVGMAGPERHOUR": 0,
                "MAGPERCREDIT": 0,
            },
        },
    }
    return2expected = {
        "ESCATTER11.FULLERTON.EDU/NFS",
        "RECHENKRAFT.NET/YOYO",
        "BOINC.MULTI-POOL.INFO/LATINSQUARES",
        "BOINC.BAKERLAB.ORG/ROSETTA",
        "UNIVERSEATHOME.PL/UNIVERSE",
        "MILKYWAY.CS.RPI.EDU/MILKYWAY",
        "EINSTEIN.PHYS.UWM.EDU",
        "SRBASE.MY-FIREWALL.ORG/SR5",
        "GPUGRID.NET",
        "GENE.DISI.UNITN.IT/TEST",
        "SIDOCK.SI/SIDOCK",
    }
    assert frozenset(list(return2)) == frozenset(return2expected)
    assert frozenset(return1) == frozenset(expected_return_1)


def test_get_most_mag_efficient_projects():
    combinedstats = {
        "WORLDCOMMUNITYGRID.ORG": {
            "COMPILED_STATS": {
                "AVGMAGPERHOUR": 1,
                "TOTALTASKS": 20,
            }
        },
        "ESCATTER11.FULLERTON.EDU/NFS": {
            "COMPILED_STATS": {
                "AVGMAGPERHOUR": 0,
                "TOTALTASKS": 10,
            }
        },
        "RECHENKRAFT.NET/YOYO": {
            "COMPILED_STATS": {
                "AVGMAGPERHOUR": 0.91,
                "TOTALTASKS": 20,
            }
        },
        "BOINC.MULTI-POOL.INFO/LATINSQUARES": {
            "COMPILED_STATS": {
                "AVGMAGPERHOUR": 1,
                "TOTALTASKS": 20,
            }
        },
    }
    ignored_projects = ["BOINC.MULTI-POOL.INFO/LATINSQUARES"]
    percentdiff = 10
    quiet: bool = True
    # test that it finds two highest projects w/ percentdiff, and that it's properly ignoring projects
    result = main.get_most_mag_efficient_projects(
        combinedstats, ignored_projects, percentdiff, quiet
    )
    assert result == ["WORLDCOMMUNITYGRID.ORG", "RECHENKRAFT.NET/YOYO"]
    # test that percentdiff is working
    percentdiff = 1
    result = main.get_most_mag_efficient_projects(
        combinedstats, ignored_projects, percentdiff, quiet
    )
    assert result == ["WORLDCOMMUNITYGRID.ORG"]


def test_get_first_non_ignored_project():
    project_list = [
        "WORLDCOMMUNITYGRID.ORG",
        "RECHENKRAFT.NET/YOYO",
        "BOINC.MULTI-POOL.INFO/LATINSQUARES",
    ]
    ignored_projects = ["RECHENKRAFT.NET/YOYO"]
    assert (
        main.get_first_non_ignored_project(project_list, ignored_projects)
        == "WORLDCOMMUNITYGRID.ORG"
    )
    ignored_projects = ["RECHENKRAFT.NET/YOYO", "WORLDCOMMUNITYGRID.ORG"]
    assert (
        main.get_first_non_ignored_project(project_list, ignored_projects)
        == "BOINC.MULTI-POOL.INFO/LATINSQUARES"
    )


def test_get_project_mag_ratios():
    # use section below if you need to update this test
    # gridcoin_conf = main.get_gridcoin_config_parameters(main.GRIDCOIN_DATA_DIR)
    # rpc_user = gridcoin_conf.get('rpcuser')
    # gridcoin_rpc_password = gridcoin_conf.get('rpcpassword')
    # rpc_port = gridcoin_conf.get('rpcport')
    # grc_client = main.GridcoinClientConnection(rpc_user=rpc_user, rpc_port=rpc_port, rpc_password=gridcoin_rpc_password)

    file = open("gridcoin/superblocks_response.txt").read()
    grc_response = json.loads(file)
    expected_answer = {
        "SECH.ME/BOINC/AMICABLE": 8.91264681577104e-05,
        "SRBASE.MY-FIREWALL.ORG/SR5": 8.539680314693781e-05,
        "SIDOCK.SI/SIDOCK": 0.003301081663199078,
        "GENE.DISI.UNITN.IT/TEST": 0.0035177177490411625,
        "WORLDCOMMUNITYGRID.ORG": 0.0009398350573579004,
        "ASTEROIDSATHOME.NET/BOINC": 0.003858841063201462,
        "EINSTEIN.PHYS.UWM.EDU": 4.0056880080044686e-05,
        "FOLDINGATHOME.DIV72.XYZ": 2.354611008478076e-05,
        "MILKYWAY.CS.RPI.EDU/MILKYWAY": 0.00017020525368876164,
        "ESCATTER11.FULLERTON.EDU/NFS": 0.0014315462447158976,
        "NUMBERFIELDS.ASU.EDU/NUMBERFIELDS": 0.0003832862658003348,
        "BOINC.MULTI-POOL.INFO/LATINSQUARES": 0.004925403380069366,
        "BOINC.BAKERLAB.ORG/ROSETTA": 0.010315385227402484,
        "UNIVERSEATHOME.PL/UNIVERSE": 0.00028549726782855914,
        "RECHENKRAFT.NET/YOYO": 0.0018665701101050107,
    }
    grc_projects = {
        "Amicable_Numbers": {
            "version": 2,
            "display_name": "Amicable Numbers",
            "url": "https://sech.me/boinc/Amicable/@",
            "base_url": "https://sech.me/boinc/Amicable/",
            "display_url": "https://sech.me/boinc/Amicable/",
            "stats_url": "https://sech.me/boinc/Amicable/stats/",
            "gdpr_controls": False,
            "time": "2023-07-14 10:58:32 UTC",
        },
        "asteroids@home": {
            "version": 2,
            "display_name": "asteroids@home",
            "url": "https://asteroidsathome.net/boinc/@",
            "base_url": "https://asteroidsathome.net/boinc/",
            "display_url": "https://asteroidsathome.net/boinc/",
            "stats_url": "https://asteroidsathome.net/boinc/stats/",
            "gdpr_controls": False,
            "time": "2023-07-14 11:01:32 UTC",
        },
        "einstein@home": {
            "version": 2,
            "display_name": "einstein@home",
            "url": "https://einstein.phys.uwm.edu/@",
            "base_url": "https://einstein.phys.uwm.edu/",
            "display_url": "https://einstein.phys.uwm.edu/",
            "stats_url": "https://einstein.phys.uwm.edu/stats/",
            "gdpr_controls": True,
            "time": "2023-07-14 11:04:33 UTC",
        },
        "folding@home": {
            "version": 2,
            "display_name": "folding@home",
            "url": "https://foldingathome.div72.xyz/@",
            "base_url": "https://foldingathome.div72.xyz/",
            "display_url": "https://foldingathome.div72.xyz/",
            "stats_url": "https://foldingathome.div72.xyz/stats/",
            "gdpr_controls": False,
            "time": "2023-07-14 11:07:33 UTC",
        },
        "milkyway@home": {
            "version": 2,
            "display_name": "milkyway@home",
            "url": "https://milkyway.cs.rpi.edu/milkyway/@",
            "base_url": "https://milkyway.cs.rpi.edu/milkyway/",
            "display_url": "https://milkyway.cs.rpi.edu/milkyway/",
            "stats_url": "https://milkyway.cs.rpi.edu/milkyway/stats/",
            "gdpr_controls": False,
            "time": "2023-07-14 11:10:33 UTC",
        },
        "nfs@home": {
            "version": 2,
            "display_name": "nfs@home",
            "url": "https://escatter11.fullerton.edu/nfs/@",
            "base_url": "https://escatter11.fullerton.edu/nfs/",
            "display_url": "https://escatter11.fullerton.edu/nfs/",
            "stats_url": "https://escatter11.fullerton.edu/nfs/stats/",
            "gdpr_controls": False,
            "time": "2023-07-14 11:13:34 UTC",
        },
        "numberfields@home": {
            "version": 2,
            "display_name": "numberfields@home",
            "url": "https://numberfields.asu.edu/NumberFields/@",
            "base_url": "https://numberfields.asu.edu/NumberFields/",
            "display_url": "https://numberfields.asu.edu/NumberFields/",
            "stats_url": "https://numberfields.asu.edu/NumberFields/stats/",
            "gdpr_controls": True,
            "time": "2023-07-14 11:16:34 UTC",
        },
        "odlk1": {
            "version": 2,
            "display_name": "odlk1",
            "url": "https://boinc.multi-pool.info/latinsquares/@",
            "base_url": "https://boinc.multi-pool.info/latinsquares/",
            "display_url": "https://boinc.multi-pool.info/latinsquares/",
            "stats_url": "https://boinc.multi-pool.info/latinsquares/stats/",
            "gdpr_controls": False,
            "time": "2023-07-14 11:19:35 UTC",
        },
        "rosetta@home": {
            "version": 2,
            "display_name": "rosetta@home",
            "url": "https://boinc.bakerlab.org/rosetta/@",
            "base_url": "https://boinc.bakerlab.org/rosetta/",
            "display_url": "https://boinc.bakerlab.org/rosetta/",
            "stats_url": "https://boinc.bakerlab.org/rosetta/stats/",
            "gdpr_controls": False,
            "time": "2023-07-14 11:22:35 UTC",
        },
        "SiDock@home": {
            "version": 2,
            "display_name": "SiDock@home",
            "url": "https://www.sidock.si/sidock/@",
            "base_url": "https://www.sidock.si/sidock/",
            "display_url": "https://www.sidock.si/sidock/",
            "stats_url": "https://www.sidock.si/sidock/stats/",
            "gdpr_controls": False,
            "time": "2023-07-14 11:25:35 UTC",
        },
        "SRBase": {
            "version": 2,
            "display_name": "SRBase",
            "url": "https://srbase.my-firewall.org/sr5/@",
            "base_url": "https://srbase.my-firewall.org/sr5/",
            "display_url": "https://srbase.my-firewall.org/sr5/",
            "stats_url": "https://srbase.my-firewall.org/sr5/stats/",
            "gdpr_controls": False,
            "time": "2023-07-14 11:28:36 UTC",
        },
        "TN-Grid": {
            "version": 2,
            "display_name": "TN-Grid",
            "url": "https://gene.disi.unitn.it/test/@",
            "base_url": "https://gene.disi.unitn.it/test/",
            "display_url": "https://gene.disi.unitn.it/test/",
            "stats_url": "https://gene.disi.unitn.it/test/stats/",
            "gdpr_controls": False,
            "time": "2023-07-14 11:31:36 UTC",
        },
        "universe@home": {
            "version": 2,
            "display_name": "universe@home",
            "url": "https://universeathome.pl/universe/@",
            "base_url": "https://universeathome.pl/universe/",
            "display_url": "https://universeathome.pl/universe/",
            "stats_url": "https://universeathome.pl/universe/stats/",
            "gdpr_controls": True,
            "time": "2023-07-14 11:34:36 UTC",
        },
        "World_Community_Grid": {
            "version": 2,
            "display_name": "World Community Grid",
            "url": "https://www.worldcommunitygrid.org/boinc/@",
            "base_url": "https://www.worldcommunitygrid.org/boinc/",
            "display_url": "https://www.worldcommunitygrid.org/",
            "stats_url": "https://www.worldcommunitygrid.org/boinc/stats/",
            "gdpr_controls": True,
            "time": "2023-07-14 11:37:37 UTC",
        },
        "yoyo@home": {
            "version": 2,
            "display_name": "yoyo@home",
            "url": "https://www.rechenkraft.net/yoyo/@",
            "base_url": "https://www.rechenkraft.net/yoyo/",
            "display_url": "https://www.rechenkraft.net/yoyo/",
            "stats_url": "https://www.rechenkraft.net/yoyo/stats/",
            "gdpr_controls": False,
            "time": "2023-07-14 11:40:37 UTC",
        },
    }
    answer = main.get_project_mag_ratios(None, 30, grc_response, grc_projects)
    assert answer == expected_answer


def test_left_align():
    my_string = "test"
    total_len = 10
    # test padding of one
    min_pad = 1
    result = main.left_align(my_string, total_len, min_pad)
    assert result == "test      "
    # test padding of zero
    min_pad = 0
    result = main.left_align(my_string, total_len, min_pad)
    assert result == "test      "
    # test padding > total_len
    total_len = 5
    min_pad = 2
    result = main.left_align(my_string, total_len, min_pad)
    assert result == "tes  "


def test_center_align():
    my_string = "test"
    total_len = 10
    # test padding of one
    min_pad = 1
    result = main.center_align(my_string, total_len, min_pad)
    assert result == "   test   "
    # test string+pad>total_len
    total_len = 9
    min_pad = 3
    result = main.center_align(my_string, total_len, min_pad)
    assert result == "   tes   "
    # test padding > total_len
    total_len = 6
    min_pad = 3
    result = main.center_align(my_string, total_len, min_pad)
    assert result == "      "


def test_ignore_message_from_check_log_entries():
    assert main.ignore_message_from_check_log_entries("WORK FETCH SUSPENDED BY USERS")


def make_fake_boinc_log_entry(
    messages: List[str], project: str
) -> List[Dict[str, str]]:
    return_list = []
    for message in messages:
        now = datetime.datetime.now()
        append_message = str(now) + " | " + project + " | " + message
        return_dict = {"time": now, "body": append_message, "project": project}
        return_list.append(return_dict)
    return return_list


def test_cache_full():
    # check it realizes both caches full
    messages = [
        "testproject CPU: JOB CACHE FULL",
        "TESTPROJECT NOT REQUESTING TASKS: DON'T NEED (JOB CACHE FULL)",
        "testproject GPU: JOB CACHE FULL",
        "testproject: GPUS NOT USABLE",
    ]
    test_messages = make_fake_boinc_log_entry(messages, "testproject")
    assert main.cache_full("testproject", test_messages)
    # make sure it's not counting other projects
    messages = [
        "testproject CPU: JOB CACHE FULL",
        "TESTPROJECT NOT REQUESTING TASKS: DON'T NEED (JOB CACHE FULL)",
        "testproject GPU: JOB CACHE FULL",
        "testproject: GPUS NOT USABLE",
    ]
    test_messages = make_fake_boinc_log_entry(messages, "testproject")
    assert not main.cache_full("anotherproject", test_messages)
    # check it realizes cpu is full on system w no gpu
    messages = ["NOT REQUESTING TASKS: DON'T NEED ()", "CPU: JOB CACHE FULL"]
    test_messages = make_fake_boinc_log_entry(messages, "testproject")
    assert main.cache_full("testproject", test_messages)


def test_project_backoff():
    messages = ["PROJECT HAS NO TASKS AVAILABLE", "SCHEDULER REQUEST FAILED"]
    test_messages = make_fake_boinc_log_entry(messages, "testproject")
    assert main.project_backoff("testproject", test_messages)
    messages = ["NOT REQUESTING TASKS: DON'T NEED", "STARTED DOWNLOAD"]
    test_messages = make_fake_boinc_log_entry(messages, "testproject")
    assert not main.project_backoff("testproject", test_messages)


def test_get_project_mag_ratios_from_response():
    file = open("gridcoin/superblocks_response.txt").read()
    response = json.loads(file)["result"]
    project_resolver_dict = {
        "Amicable_Numbers": "SECH.ME/BOINC/AMICABLE",
        "asteroids@home": "ASTEROIDSATHOME.NET/BOINC",
        "einstein@home": "EINSTEIN.PHYS.UWM.EDU",
        "folding@home": "FOLDINGATHOME.DIV72.XYZ",
        "milkyway@home": "MILKYWAY.CS.RPI.EDU/MILKYWAY",
        "nfs@home": "ESCATTER11.FULLERTON.EDU/NFS",
        "numberfields@home": "NUMBERFIELDS.ASU.EDU/NUMBERFIELDS",
        "odlk1": "BOINC.MULTI-POOL.INFO/LATINSQUARES",
        "rosetta@home": "BOINC.BAKERLAB.ORG/ROSETTA",
        "SiDock@home": "SIDOCK.SI/SIDOCK",
        "SRBase": "SRBASE.MY-FIREWALL.ORG/SR5",
        "TN-Grid": "GENE.DISI.UNITN.IT/TEST",
        "universe@home": "UNIVERSEATHOME.PL/UNIVERSE",
        "World_Community_Grid": "WORLDCOMMUNITYGRID.ORG/BOINC",
        "yoyo@home": "RECHENKRAFT.NET/YOYO",
    }
    lookback_period = 30
    result = main.get_project_mag_ratios_from_response(
        response, lookback_period, project_resolver_dict
    )
    assert result == {
        "SECH.ME/BOINC/AMICABLE": 8.91264681577104e-05,
        "SRBASE.MY-FIREWALL.ORG/SR5": 8.539680314693781e-05,
        "SIDOCK.SI/SIDOCK": 0.003301081663199078,
        "GENE.DISI.UNITN.IT/TEST": 0.0035177177490411625,
        "WORLDCOMMUNITYGRID.ORG": 0.0009398350573579004,
        "ASTEROIDSATHOME.NET/BOINC": 0.003858841063201462,
        "EINSTEIN.PHYS.UWM.EDU": 4.0056880080044686e-05,
        "FOLDINGATHOME.DIV72.XYZ": 2.354611008478076e-05,
        "MILKYWAY.CS.RPI.EDU/MILKYWAY": 0.00017020525368876164,
        "ESCATTER11.FULLERTON.EDU/NFS": 0.0014315462447158976,
        "NUMBERFIELDS.ASU.EDU/NUMBERFIELDS": 0.0003832862658003348,
        "BOINC.MULTI-POOL.INFO/LATINSQUARES": 0.004925403380069366,
        "BOINC.BAKERLAB.ORG/ROSETTA": 0.010315385227402484,
        "UNIVERSEATHOME.PL/UNIVERSE": 0.00028549726782855914,
        "RECHENKRAFT.NET/YOYO": 0.0018665701101050107,
    }


def test_profitability_check():
    # profitable if you sell GRC for a 1000 USD
    grc_price = 0.00
    exchange_fee = 0.10
    main.HOST_COST_PER_HOUR = 1
    grc_sell_price = 1000
    min_profit_per_hour = 0
    combined_stats = {"myproject.com": {"COMPILED_STATS": {"AVGMAGPERHOUR": 4}}}
    assert main.profitability_check(
        grc_price,
        exchange_fee,
        grc_sell_price,
        "myproject.com",
        min_profit_per_hour,
        combined_stats,
    )
    # not profitable if grc is worth zero
    grc_sell_price = 0
    assert not main.profitability_check(
        grc_price,
        exchange_fee,
        grc_sell_price,
        "myproject.com",
        min_profit_per_hour,
        combined_stats,
    )
    # not profitable if expenses too high
    main.HOST_COST_PER_HOUR = 10
    grc_sell_price = 1
    assert not main.profitability_check(
        grc_price,
        exchange_fee,
        grc_sell_price,
        "myproject.com",
        min_profit_per_hour,
        combined_stats,
    )


def test_get_avg_mag_hr():
    combined_stats = {
        "myproject.com": {"COMPILED_STATS": {"TOTALWALLTIME": 1, "AVGMAGPERHOUR": 2}},
        "myproject2.com": {"COMPILED_STATS": {"TOTALWALLTIME": 1, "AVGMAGPERHOUR": 2}},
    }
    result = main.get_avg_mag_hr(combined_stats)
    assert result == 2


def test_make_discrepancy_timeout():
    original_dev_mode = main.FORCE_DEV_MODE
    main.FORCE_DEV_MODE = True
    answer = main.make_discrepancy_timeout(-100)
    assert answer == 60
    main.FORCE_DEV_MODE = False
    answer = main.make_discrepancy_timeout(-60)
    assert answer == 0
    answer = main.make_discrepancy_timeout(100)
    assert answer == 100
    main.FORCE_DEV_MODE == original_dev_mode


def test_owed_to_dev():
    original_ftm_total = None
    if main.DATABASE.get("FTMTOTAL"):
        original_ftm_total = main.DATABASE.get("FTMTOTAL")
    original_dev_total = None
    if main.DATABASE.get("DEVTIMETOTAL"):
        original_dev_total = main.DATABASE.get("DEVTIMETOTAL")
    main.DEV_FEE = 0.01
    # negative hours owed
    main.DATABASE["FTMTOTAL"] = 100 * 60
    main.DATABASE["DEVTIMETOTAL"] = 10 * 60
    discrepancy = main.owed_to_dev()
    assert discrepancy == -8.9
    # 9.01 hr owed
    main.DATABASE["FTMTOTAL"] = 1000 * 60
    main.DATABASE["DEVTIMETOTAL"] = 1 * 60
    discrepancy = main.owed_to_dev()
    assert discrepancy == 9.01
    # restore original values
    if original_ftm_total:
        main.DATABASE["FTMTOTAL"] = original_ftm_total
    if original_dev_total:
        main.DATABASE["DEVTOTAL"] = original_dev_total


def test_date_to_date():
    original_date = "06-26-2023"
    converted = main.date_to_date(original_date)
    assert converted.year == 2023
    assert converted.month == 6
    assert converted.day == 26


def test_get_latest_wu_date():
    dates = ["06-26-2023", "06-27-2024", "06-23-2022"]
    latest_date = main.get_latest_wu_date(dates)
    assert latest_date.year == 2024


def test_stuck_xfer():
    example_xfer = {
        "status": "1",
        "persistent_file_xfer": {
            "num_retries": 1,
        },
    }
    assert main.stuck_xfer(example_xfer)
    example_xfer = {
        "status": "0",
        "persistent_file_xfer": {
            "num_retries": 1,
        },
    }
    assert main.stuck_xfer(example_xfer)
    example_xfer = {
        "status": "0",
        "persistent_file_xfer": {
            "num_retries": 0,
        },
    }
    assert not main.stuck_xfer(example_xfer)
    example_xfer = {
        "status": "0",
    }
    assert not main.stuck_xfer(example_xfer)


def test_json_default():
    return_dict = main.json_default(datetime.datetime.now())
    assert isinstance(return_dict, dict)


def test_object_hook():
    return_dict = main.json_default(datetime.datetime.now())
    result = main.object_hook(return_dict)
    assert isinstance(result, datetime.datetime)


def test_should_crunch_for_dev():
    original_dev_mode = main.FORCE_DEV_MODE
    main.DEV_FEE = 0.01
    # should return false is in dev loop
    assert not main.should_crunch_for_dev(True)
    # should return false if user is sidestaking
    main.CHECK_SIDESTAKE_RESULTS = True
    assert not main.should_crunch_for_dev(False)
    # should return True if dev mode forced
    main.CHECK_SIDESTAKE_RESULTS = False
    main.FORCE_DEV_MODE = True
    assert main.should_crunch_for_dev(False)
    # should return True if due to crunch
    main.FORCE_DEV_MODE = False
    main.DATABASE["FTMTOTAL"] = 100000 * 60
    main.DATABASE["DEVTIMETOTAL"] = 1 * 60
    assert main.should_crunch_for_dev(False)
    # should return True if not due to crunch
    main.FORCE_DEV_MODE = False
    main.DATABASE["FTMTOTAL"] = 98 * 60
    main.DATABASE["DEVTIMETOTAL"] = 1 * 60
    assert not main.should_crunch_for_dev(False)
    # return originals
    main.FORCE_DEV_MODE = original_dev_mode
