# CHANGELOG



## v2.2.0 (2024-06-28)

### Feature

* feat: switch to github trusted publishing (#54) ([`d5bae3f`](https://github.com/bdraco/aiodiscover/commit/d5bae3f0fefb3f30aa9d63c79d19fdc96d116eff))


## v2.1.0 (2024-04-18)

### Unknown

* Bump version: 2.0.0 → 2.1.0 ([`2e79d02`](https://github.com/bdraco/aiodiscover/commit/2e79d022a2f6cc854cd3adbee02ccc75a90336eb))

* Rate limit queries to reduce load on DNS servers (#45) ([`29bc9c6`](https://github.com/bdraco/aiodiscover/commit/29bc9c6f5c6d5253ab08db39067f4c268521df9b))


## v2.0.0 (2024-03-13)

### Unknown

* Bump version: 1.6.1 → 2.0.0 ([`a4fc87f`](https://github.com/bdraco/aiodiscover/commit/a4fc87fa3249ae73b08fde1b02ab6d63658d6edf))

* Switch dns resolver to use aiodns (#44) ([`9132a13`](https://github.com/bdraco/aiodiscover/commit/9132a13abf5e142476111e73adbc7f9f893c6235))

* Cache network information instead of fetching it each time (#43) ([`cdbb9b4`](https://github.com/bdraco/aiodiscover/commit/cdbb9b4d605a164cbae1c564af9e3b5b6d39a424))


## v1.6.1 (2024-02-08)

### Fix

* fix: decode ptr names as unicode (#40) ([`e1533d9`](https://github.com/bdraco/aiodiscover/commit/e1533d9979d96b7180d9979992afa9485a50f18d))

### Unknown

* Bump version: 1.6.0 → 1.6.1 ([`9d572f9`](https://github.com/bdraco/aiodiscover/commit/9d572f9cc4d58911be3a5925274cb6c2bab6679a))


## v1.6.0 (2023-12-16)

### Feature

* feat: improve performance with cached_ipaddress (#38) ([`20b1fe6`](https://github.com/bdraco/aiodiscover/commit/20b1fe6b92359a7439c0f92d400c4b9be8c178f3))

### Unknown

* Bump version: 1.5.1 → 1.6.0 ([`decb249`](https://github.com/bdraco/aiodiscover/commit/decb249a746740b94b04d04b763880e5d50791f5))


## v1.5.1 (2023-09-09)

### Unknown

* Bump version: 1.5.0 → 1.5.1 ([`2261122`](https://github.com/bdraco/aiodiscover/commit/2261122a1390f9eb3f074e4b213867fb486f1c6c))


## v1.5.0 (2023-09-09)

### Unknown

* Bump version: 1.4.16 → 1.5.0 ([`965843e`](https://github.com/bdraco/aiodiscover/commit/965843e39228a48f38f80effddb5598db78197cd))

* Improve performance of timeout behavior (#37) ([`79acf11`](https://github.com/bdraco/aiodiscover/commit/79acf115b5616a670d252987e611814c6449f08c))


## v1.4.16 (2023-04-05)

### Unknown

* Bump version: 1.4.15 → 1.4.16 ([`7809bdf`](https://github.com/bdraco/aiodiscover/commit/7809bdfd8b56e28318becdd23ac24f9b25df801e))

* Bump dnspython to 2.3.0 (#36) ([`9fd228f`](https://github.com/bdraco/aiodiscover/commit/9fd228f707c76cbebcc0b48b5eaa778220fafd3f))


## v1.4.15 (2023-03-27)

### Unknown

* Bump version: 1.4.14 → 1.4.15 ([`ee81c58`](https://github.com/bdraco/aiodiscover/commit/ee81c585d5f8b473ea322243e26f0293f514acd0))

* Reduce overhead to get arp table on macos (#35) ([`7affeff`](https://github.com/bdraco/aiodiscover/commit/7affeff610737612589f816bb9d2dc6d43ad5667))


## v1.4.14 (2023-03-04)

### Unknown

* Bump version: 1.4.13 → 1.4.14 ([`a6ea77f`](https://github.com/bdraco/aiodiscover/commit/a6ea77fdf2e8e3248c3b625d00931b6ca5443dea))

* Add python 3.11 (#34) ([`702d2da`](https://github.com/bdraco/aiodiscover/commit/702d2da5c67828d4e7d649175fb4f2f7872884d3))

* Switch pr2modules to pyroute2 (#33) ([`1c33dc4`](https://github.com/bdraco/aiodiscover/commit/1c33dc4ac0b13cafd66e09024d9ee2c68e01f2b0))

* Cache name construction of dns PTRs (#32) ([`9de198a`](https://github.com/bdraco/aiodiscover/commit/9de198a181c6cfa94ba74432711997f598fb175b))


## v1.4.13 (2022-09-11)

### Unknown

* Bump version: 1.4.12 → 1.4.13 ([`0ab707c`](https://github.com/bdraco/aiodiscover/commit/0ab707ca4b7e8976060e77449194ddfe07d0444d))


## v1.4.12 (2022-09-11)

### Unknown

* Bump version: 1.4.11 → 1.4.12 ([`647b0f0`](https://github.com/bdraco/aiodiscover/commit/647b0f00a21305339898dc6cd2efb0d8e8d90a4a))

* Improve performance by switching to async_timeout (#29) ([`77a3e04`](https://github.com/bdraco/aiodiscover/commit/77a3e0424ab14029084ff830bad9893be462b5eb))


## v1.4.11 (2022-04-21)

### Unknown

* Bump version: 1.4.10 → 1.4.11 ([`4a3e1af`](https://github.com/bdraco/aiodiscover/commit/4a3e1af8ddce2425b8729e0ba4d213e09b33099b))

* Fix KeyError when dns server does not respond for a single ip (#28) ([`b6c5b4b`](https://github.com/bdraco/aiodiscover/commit/b6c5b4b364c16e08bacc7ccf2929e9d26b0af944))


## v1.4.10 (2022-04-20)

### Unknown

* Bump version: 1.4.9 → 1.4.10 ([`fffad51`](https://github.com/bdraco/aiodiscover/commit/fffad516495f9e7cddd653d896a9be03f3372e94))

* Use new lighter pyroute import to reduce memory RSS ~11m (#27) ([`82a8174`](https://github.com/bdraco/aiodiscover/commit/82a8174fa49096ccf2191588d63dfbfdd25eb6d5))


## v1.4.9 (2022-04-17)

### Unknown

* Bump version: 1.4.8 → 1.4.9 ([`feb1ce8`](https://github.com/bdraco/aiodiscover/commit/feb1ce846e3b6adaa39160e64006710c69a5e0ed))

* Add fallback for finding source ip (#26) ([`3e8f253`](https://github.com/bdraco/aiodiscover/commit/3e8f25358d93e8c4fb464e4f615d262766d70d90))


## v1.4.8 (2022-02-19)

### Unknown

* Bump version: 1.4.7 → 1.4.8 ([`0d69cf2`](https://github.com/bdraco/aiodiscover/commit/0d69cf284741b6cc797cfc9c27390d6524566360))

* Load IPRoute in the executor (#24) ([`7609b5d`](https://github.com/bdraco/aiodiscover/commit/7609b5d5cf3309c842184b563111571d4f11ae74))


## v1.4.7 (2022-01-24)

### Unknown

* Bump version: 1.4.6 → 1.4.7 ([`6a131d9`](https://github.com/bdraco/aiodiscover/commit/6a131d9244d127c966c3419e7f401642a1a9047f))


## v1.4.6 (2022-01-24)

### Unknown

* Bump version: 1.4.5 → 1.4.6 ([`4502040`](https://github.com/bdraco/aiodiscover/commit/45020400367e0a5c1a3f578c6229864961710e80))

* Fix getting the default gateway on MacOS (#23) ([`fd570e4`](https://github.com/bdraco/aiodiscover/commit/fd570e44fb4b5a51f6e907ef640858d40aa3e2a5))


## v1.4.5 (2021-10-10)

### Unknown

* Bump version: 1.4.4 → 1.4.5 ([`00bb409`](https://github.com/bdraco/aiodiscover/commit/00bb4094fdfa58ba4f9729de6dfa7d95efb67a80))

* Fix publish workflow (#22) ([`3a10847`](https://github.com/bdraco/aiodiscover/commit/3a1084731a0bf98a04f189708329f1f12e76e7ef))

* Add python 3.10 to the CI (#21) ([`ac21028`](https://github.com/bdraco/aiodiscover/commit/ac21028b15cbe014bf889dfaf9c9dfefd1c951af))

* Skip scanning when the network size exceeds MAX_ADDRESSES (8192) (#20) ([`207c6ea`](https://github.com/bdraco/aiodiscover/commit/207c6ea9c10d1f84bf9eac4052a55ae827725328))


## v1.4.4 (2021-09-29)

### Unknown

* Bump version: 1.4.3 → 1.4.4 ([`ebbcf4f`](https://github.com/bdraco/aiodiscover/commit/ebbcf4f20236467ad5e4d0b7422b06ed7520f238))


## v1.4.3 (2021-09-29)

### Unknown

* Bump version: 1.4.2 → 1.4.3 ([`7f84a6f`](https://github.com/bdraco/aiodiscover/commit/7f84a6f946870a72fb8bd633de3cff4a61886722))

* Ensure mac addresses with leading zeros are not striped (#19) ([`3980bac`](https://github.com/bdraco/aiodiscover/commit/3980bac804720dc2e06b6ab4aeb74f95880d58ec))


## v1.4.2 (2021-05-20)

### Unknown

* Bump version: 1.4.1 → 1.4.2 ([`f24492e`](https://github.com/bdraco/aiodiscover/commit/f24492e6497c561db50d509edb61d0309d8f61f8))

* Update publish flow ([`5f32738`](https://github.com/bdraco/aiodiscover/commit/5f327385e3cac752e16b00ae831c703eee0a2d67))


## v1.4.1 (2021-05-20)

### Unknown

* Bump version: 1.4.0 → 1.4.1 ([`3c8bc4b`](https://github.com/bdraco/aiodiscover/commit/3c8bc4ba00758b90c27cfafc3f4f891c285209c7))

* Use built-in ip.reverse_pointer (#18) ([`d074246`](https://github.com/bdraco/aiodiscover/commit/d074246e38a4d54cc032b4b39605af3ec1c25c89))


## v1.4.0 (2021-04-17)

### Unknown

* Bump version: 1.3.4 → 1.4.0 ([`96b028d`](https://github.com/bdraco/aiodiscover/commit/96b028d94bc7be36c91ead17c5c835dbf9f10785))

* Switch to dnspython from async_dns (#17)

- async_dns was writing configuration files under the hood when loading the library ([`067ca0b`](https://github.com/bdraco/aiodiscover/commit/067ca0b8c468f2a66d1b423e28ec95da094d03f1))

* Bump version: 1.3.3 → 1.3.4 (#16) ([`a76c999`](https://github.com/bdraco/aiodiscover/commit/a76c9990d7c8f343ad76bd78ee90e0bbdbea39c5))

* Bump pyroute2 version to &gt;=0.5.18 (#15) ([`a10a591`](https://github.com/bdraco/aiodiscover/commit/a10a59132452b7630fa10df97b98df5600255dea))


## v1.3.3 (2021-04-02)

### Unknown

* Bump version: 1.3.2 → 1.3.3 ([`b4edcd9`](https://github.com/bdraco/aiodiscover/commit/b4edcd9dfdd233ebe09492eda21bf80458ef1195))

* Scan the /24 if we cannot determine the network prefix (#14) ([`4441656`](https://github.com/bdraco/aiodiscover/commit/444165606cbe6d31f5b6d8443923da1dc5e1abba))

* Increase coverage for exception during ptr query (#13) ([`6db8e3f`](https://github.com/bdraco/aiodiscover/commit/6db8e3f4d5f672bfe7745f5e64edae64169db943))

* Increase ptr resolver coverage for error case (#12) ([`33b4cb0`](https://github.com/bdraco/aiodiscover/commit/33b4cb0a8ff97ba261ac5956f74bc6ee6e1fbfcd))

* Abort ptr discovery on error_received (#11) ([`ce97a01`](https://github.com/bdraco/aiodiscover/commit/ce97a016876aa948c404f3b32df1695e7d443a4a))

* Abort ptr discovery on error_received (#10) ([`ad5da63`](https://github.com/bdraco/aiodiscover/commit/ad5da6321f9a0fb2528c26238f68111af3af84b9))

* Remove entry_point (#9) ([`7ac0987`](https://github.com/bdraco/aiodiscover/commit/7ac09878e28b8e002946572dd2f0d042bf9f5a1f))


## v1.3.2 (2021-03-29)

### Unknown

* Bump version: 1.3.1 → 1.3.2 ([`765e5b1`](https://github.com/bdraco/aiodiscover/commit/765e5b1f44754f102b10eb81e2b309e87526dac2))

* Remove unused utils code (#8) ([`760995f`](https://github.com/bdraco/aiodiscover/commit/760995f13e371668994cdc5f3c6e0f978a14a6c2))


## v1.3.1 (2021-03-29)

### Unknown

* Bump version: 1.3.0 → 1.3.1 ([`70d321f`](https://github.com/bdraco/aiodiscover/commit/70d321f6add816915728b02e7aa91e1b4681268a))

* Fix slow memory leak on connection lost (#7) ([`7f39e99`](https://github.com/bdraco/aiodiscover/commit/7f39e99db87ebce007c6ff49154f584da947d14e))


## v1.3.0 (2021-03-29)

### Unknown

* Bump version: 1.2.0 → 1.3.0 ([`8839893`](https://github.com/bdraco/aiodiscover/commit/883989355924aa7ec61b582c9845245134126d07))

* Improve version test (#6) ([`d04a2ed`](https://github.com/bdraco/aiodiscover/commit/d04a2ed81acc8785824382ee9e760b5d3380e0a2))

* Increase coverage (#5) ([`84c6d01`](https://github.com/bdraco/aiodiscover/commit/84c6d01806033d0b3b0a923d951fcc0242875dbc))

* Significantly reduce cpu time required for PTR lookups by reusing the datagram endpoint (#4)

- In testing this was roughly 2 orders of magnitude less cpu time used ([`fd8cee0`](https://github.com/bdraco/aiodiscover/commit/fd8cee0da50f3b9fde86c1ecea13c6623ab5b53d))


## v1.2.0 (2021-03-28)

### Unknown

* Bump version: 1.1.2 → 1.2.0 ([`852a780`](https://github.com/bdraco/aiodiscover/commit/852a780032b415be63509bb9b81ce32951ca5fef))

* Optimize ARP cache population (#3)

- Use a single non-blocking socket to populate the arp cache
- Add a profiler script: profile_discovery.py
- Avoid populating the arp cache if it already exists
- Loosen MAC address validation to handle leading 0s and short format
- Run ip_route.get_neighbours in the executor. ([`5c3cbfa`](https://github.com/bdraco/aiodiscover/commit/5c3cbfaccfa6f49679257e2d996f095584ee056c))


## v1.1.2 (2021-03-28)

### Unknown

* Bump version: 1.1.1 → 1.1.2 ([`c859d6a`](https://github.com/bdraco/aiodiscover/commit/c859d6a7895edef0d0111e6c70bd74bb3026badd))

* Bump version: 1.1.0 → 1.1.1 ([`011c7ea`](https://github.com/bdraco/aiodiscover/commit/011c7ead1cf33b93051f1a33a55165ac78909fbe))

* Optimize for systems with many nameservers in resolv.conf (#2) ([`39adb33`](https://github.com/bdraco/aiodiscover/commit/39adb33e3e4895efa08c4b66e70fb5287a85ca9d))


## v1.1.0 (2021-03-28)

### Unknown

* Bump version: 1.0.1 → 1.1.0 ([`2f9b174`](https://github.com/bdraco/aiodiscover/commit/2f9b17424aed20e54e7fe0732de3044577f06791))

* Optimize to only check for neighbors that have a PTR (#1) ([`34a09b3`](https://github.com/bdraco/aiodiscover/commit/34a09b3b283a1bc59e52c4d01af9eca16472c692))


## v1.0.1 (2021-03-27)

### Unknown

* Bump version: 1.0.0 → 1.0.1 ([`37f1aa6`](https://github.com/bdraco/aiodiscover/commit/37f1aa65871314c4a1f98d3d9493ba5d6ba582b0))

* add missing file ([`a7b71d0`](https://github.com/bdraco/aiodiscover/commit/a7b71d0e54c3a3001466cd3c45a603e65a610554))

* remove ping ([`426d0b4`](https://github.com/bdraco/aiodiscover/commit/426d0b428d8153eefaae381697eaa5d275ec19af))

* handle w32 ([`a9f38b2`](https://github.com/bdraco/aiodiscover/commit/a9f38b2855af3b1e306d116b0c76541f13f9c149))

* more macos fixes ([`65f95b7`](https://github.com/bdraco/aiodiscover/commit/65f95b77a8f9c67ba3da54a9c7175b7435c8d4de))

* macos ([`fa9a535`](https://github.com/bdraco/aiodiscover/commit/fa9a535868e62a9c89bff5a044ca921b15de78c6))

* macos ([`35b4363`](https://github.com/bdraco/aiodiscover/commit/35b436361de5855cd4942d36f522cd553e8b5d84))

* win32 ([`8c4b90a`](https://github.com/bdraco/aiodiscover/commit/8c4b90a0ddee0b425744311becf84b19824730c3))

* add demo ([`3a99fbd`](https://github.com/bdraco/aiodiscover/commit/3a99fbdb9d0b4bd6dd3923266933427e8fa633bc))

* Fix macos ([`507da64`](https://github.com/bdraco/aiodiscover/commit/507da64983ff190590bd8f79104ff3a79fe639a5))

* Fix macos ([`46b656f`](https://github.com/bdraco/aiodiscover/commit/46b656ff1ffd40a48a30e2f1aca92212374fafad))

* Fix macos ([`f7a588b`](https://github.com/bdraco/aiodiscover/commit/f7a588b39169b80ecba85accc73f2db91e45396f))

* Fix macos ([`2e51271`](https://github.com/bdraco/aiodiscover/commit/2e51271dc38aeb29e1f1ee60d175da68cae27091))

* Fix resolv.conf parser ([`1a576c1`](https://github.com/bdraco/aiodiscover/commit/1a576c1eb67870c4589866a9b425509c458cb0ea))

* Fix test ([`b9afdeb`](https://github.com/bdraco/aiodiscover/commit/b9afdeb0fbe678fff77e57e5cb7a28512d8a8c29))

* require pytest-asyncio ([`502e604`](https://github.com/bdraco/aiodiscover/commit/502e6047ca3fde4cff46360fc50b7065ae632d85))

* fix requires ([`7ea23b7`](https://github.com/bdraco/aiodiscover/commit/7ea23b7a4578859f32dacd1654a9ae3e6ccf0abb))

* Merge branch &#39;main&#39; of github.com:bdraco/aiodiscover into main ([`a07fb8f`](https://github.com/bdraco/aiodiscover/commit/a07fb8f9c64574f09acf6e9a6d58f0a4fe33b1aa))

* Update README.md ([`cac731b`](https://github.com/bdraco/aiodiscover/commit/cac731b29e76266bc5797b820491e20606e20076))

* Update README.md ([`e2ebf6f`](https://github.com/bdraco/aiodiscover/commit/e2ebf6f36b556d1b9a98c4860114e39ed31cdbaf))

* Remove boiler plate ([`b729657`](https://github.com/bdraco/aiodiscover/commit/b729657393419cb05457cc7df30ccef92da8a9e7))

* Import code ([`d1db9a7`](https://github.com/bdraco/aiodiscover/commit/d1db9a79df7c56b7930f04a79a36c2360ce8cd18))

* Initial commit ([`0affef0`](https://github.com/bdraco/aiodiscover/commit/0affef0458a584b9674b2fd6ca4444f5e1edbc63))
