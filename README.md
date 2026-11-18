\# Endpoint Coverage Check



A Python control test that compares an asset inventory with an endpoint

monitoring export and generates a per-asset evidence report.



\## Risk and control objective



Endpoints without active monitoring may leave security events undetected.

Each in-scope endpoint should have an agent reported as active.



\## How to run



Requires Python 3. On Windows, run this command from the project folder:



```powershell

py -3 .\\check\_coverage.py

```



The script reads `inventory.csv` and `agents.csv` and writes

`coverage\_report.csv`.



\## Verified example



The included synthetic dataset produced \*\*25% confirmed coverage (1 of 4)\*\*.



| Asset | Result | Reason |

| --- | --- | --- |

| `lab-win-01` | PASS | Agent reported active |

| `lab-linux-01` | FAIL | Agent reported disconnected |

| `lab-win-02` | FAIL | No matching agent record |

| `lab-linux-02` | INCONCLUSIVE | Agent status requires verification |



\## Remediation



Investigate disconnected agents, verify enrollment for assets without a

matching record, and validate unknown statuses with the monitoring owner.



\## Evidence scope



Coverage is the number of in-scope assets with an active agent divided by

the total number of in-scope assets. The result reflects the supplied CSV

snapshots and depends on their completeness, freshness, and asset ID mapping.

