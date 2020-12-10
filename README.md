# GTFS2Liniennetz
Creates beautiful transport maps ("Liniennetze") from GTFS public transport data.

The created transport maps are exported as SVG and can be viewed by any browser and can be modified or exported to other formats by any good vector graphics manipulation program (such as Inkscape, Affinity Designer or Adobe Illustrator).

# Examples
KVB Köln (Cologne), Germany:

<img src="./img/kvb.svg?raw=true" height="500" alt="Transport map of KVB Cologne trams">

GVB Amsterdam, Netherlands:

<img src="./img/gvb.svg?raw=true" height="500" alt="Transport map of GVB Amsterdam">

Trains in the Netherlands (Intercity with bold lines, local trains in thin, unicolor lines):

<img src="./img/nl-trein.svg?raw=true" height="500" alt="Transport map of trains in the Netherlands">

Long-distance trains in Germany:

<img src="./img/db-fv.svg?raw=true" height="500" alt="Transport map of long-distance trains in Germany">


More examples can be found in the `img` folder.

# Getting started
## Step 1: Filter GTFS data set
Most GTFS data sets are quite large. It is thus reasonable to filter out unnecessary parts of it.

1. Create a folder `data-raw` on root level of this project where you place your unpacked GTFS data set. Make sure that the txt-files are not directly in `data-raw` but inside another folder.
2. Open the existing python file `gtfs-filter.py` and configure it as follows:
  * Change the value of `INPUT_DIR` to the name of the folder inside `data-raw`.
  * Change the value of `OUTPUT_DIR` to a desired output folder name. The filtered data will be exported to `data/{OUTPUT_DIR}`.
  * Change `DATE` to a date in the format YYYYMMDD. All other dates in the data set will be filtered out.
  * Adapt the provided functions `AGENCY_FILTER` and `ROUTE_FILTER` to filter for agencies (Verkehrsunternehmen) and routes (Linien). If you don’t want to filter at all, just make these functions always return `True`.
3. Run `gtfs-filter.py` with
  ```
  python3 gtfs-filter.py
  ```
  Depending on the size of your data set, this might take a while. After that a folder with the specified output-dir name should be appeared in the `data` folder.
  
## Step 2: Create the transport map
Create a python file on the project root named `network_YOUR_NETWORK_NAME.py`. Into this file paste the following content:
```python
import visstart
from NetworkConfig import NetworkConfig

config = NetworkConfig("YOUR_FILTERED_GTFS_FOLDER_NAME")

# You can configure your transport map here

visstart.start(config)
```
Change `YOUR_FILTERED_GTFS_FOLDER_NAME` to the name of the GTFS folder inside `data` and run this python script with:
```
python3 network_YOUR_NETWORK_NAME.py
```
Inside the `img` folder, an SVG file with the same name as the SVG should appear.

Congratulations! You have just created your first transport map. 🎉

## Step 3: Configure the transport map
If you are already happy with the result from Step 2, you can stop now. But you’re probably not, so read on to get to know how to tailor the transport maps to your expectations!

Although the configuration of the transport map creation already has reasonalbe default values, they probably don’t fill all. This is mainly because the each public transport network looks different and has a different structure. In the pasted code snippet it is already indicated where you can configure the look of your transport map. Simply set the attributes of `config`. For example, if you want to change the line width to 1px, just add a `config.line_width = 1` there and rerun the script. In `NetworkConfig.py` all configurable attributes are listed together with their default values. In the future I will also create an overview here.

# Where can I find GTFS data?
Just google for "GTFS" plus your favorite public transport operator/association (Verkehrsunternehmen/-verbund)! 😉

Here some examples which are used for the examples above:

  * [VRS Verkehrsverbund Rhein/Sieg (region Cologne/Bonn)](https://www.vrs.de/fahren/fahrplanauskunft/opendata-/-openservice)
  * [DELFI Public transport data from whole Germany](https://www.opendata-oepnv.de/ht/de/organisation/delfi/startseite?tx_vrrkit_view%5Bdataset_name%5D=deutschlandweite-sollfahrplandaten-gtfs&tx_vrrkit_view%5Baction%5D=details&tx_vrrkit_view%5Bcontroller%5D=View)
  * [OVApi Netherlands](http://gtfs.ovapi.nl/)
