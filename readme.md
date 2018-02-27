# SAP PyRFC

## Getting Started

Clone the repo or download as a zipfile and extract it to your project folder.


### Prerequisites

This project is dependent on the pyrfc library (you can get it here: https://github.com/SAP/PyRFC).
* The DLL required for the pyrfc module is proprietary. *


### Installing

After installing the pyrfc library, you should enter the credentials for your server in the main function:

 ```

    def __init__(self):
        self.conn = Connection(user='USER',
                               passwd='PASS',
                               ashost='AHOST',
                               sysnr='SYSNR',
                               client='CLIENT',
                               lang='EN')

```

### Example

Go ahead and invoke the main function:

```
from SAP_PyRFC import main

sap = main()

```

After this you can call the functions of the class. The below example will create a SQL Where clause, for the 'TRKORR' field for every transport in a list.

```
Where = sap.whereclauses(fieldname='TRKORR',qrylist=listoftransports)

```

After creating the where clause, you can query sap. The below example will query the E070 table, using our where clause. It will only return the values of the AS4DATE field.

```
Creationdatedict = sap.qry(Fields=['AS4DATE'],SQLTable='E070',Where=Where)

```

I included a sample script that I used to look for object contention in process chains. The example gives more in-depth information regarding the functions.

## Contributing

Please feel free to contribute, in case of any question please contact CRealCode@Gmail.com