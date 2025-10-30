# API Endpoints

| Method | Endpoint Path | Description | Basic | Full |
| :--- | :--- | :--- | :---: | :---: |
| GET | /HealthCheck | Checks ASF health status. | ✅ | |
| GET | /ASF | Fetches common info related to ASF as a whole. | ✅ | |
| POST | /ASF | Updates ASF's global configuration. | ✅ | |
| POST | /ASF/Exit | Shuts down ASF. | ✅ | |
| POST | /ASF/Restart | Restarts ASF. | ✅ | |
| GET | /Bot/{botNames} | Fetches information about specified bots. | ✅ | ✅ |
| POST | /Bot/{botNames} | Updates configuration of specified bots. | ✅ | |
| DELETE | /Bot/{botNames} | Deletes all files related to specified bots. | ✅ | |
| POST | /Bot/{botNames}/Start | Starts specified bots. | ✅ | |
| POST | /Bot/{botNames}/Stop | Stops specified bots. | ✅ | |
| POST | /Bot/{botNames}/Pause | Pauses specified bots. | ✅ | |
| POST | /Bot/{botNames}/Resume | Resumes specified bots. | ✅ | |
| POST | /Bot/{botNames}/Redeem | Redeems cd-keys on specified bots. | ✅ | ✅ |
| POST | /Bot/{botNames}/AddLicense | Adds free licenses on specified bots. | ✅ | |
| GET | /Bot/{botNames}/Inventory | Fetches inventory information of specified bots. | ✅ | |
| GET | /Bot/{botNames}/Inventory/{appID}/{contextID} | Fetches specific app inventory of specified bots. | ✅ | |
| POST | /Bot/{botNames}/Input | Provides input value to bot for next usage. | ✅ | |
| POST | /Bot/{botName}/Rename | Renames bot along with all related files. | ✅ | |
| GET | /Bot/{botNames}/GamesToRedeemInBackground | Fetches background game redeemer output. | ✅ | |
| POST | /Bot/{botNames}/GamesToRedeemInBackground | Adds keys to background game redeemer. | ✅ | |
| DELETE | /Bot/{botNames}/GamesToRedeemInBackground | Removes background game redeemer output files. | ✅ | |
| POST | /Bot/{botNames}/RedeemPoints/{definitionID} | Redeems points on specified bots. | ✅ | |
| GET | /Bot/{botNames}/TwoFactorAuthentication/Token | Fetches 2FA tokens of given bots. | ✅ | |
| POST | /Command | Executes a command (LEGACY). | ✅ | ✅ |
| GET | /NLog/File | Fetches ASF log file. | ✅ | |
| GET | /NLog | Establishes WebSocket connection for real-time logs. | ✅ | |
| GET | /Structure/{structure} | Fetches default structure of a given type. | ✅ | |
| GET | /Type/{type} | Fetches type information for a given type. | ✅ | |
