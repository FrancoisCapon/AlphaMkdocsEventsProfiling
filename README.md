# Alpha Mkdocs Events Profiling

## Install the Package

* Load the module and install it 
```
python3 setup.py install
```


## Profil a build

* Add the `fc-events-profiling/` to directories
```
docs/
fc-events-profiling/
site/
mkdocs.yml
```
* Add the plugin in the last position and `build`
```yaml
plugins:
  - search
# FC pip3 install mkdocs-exclude
  - exclude:
      glob:
        - "**/include-*.md"       
  - fc_events_profiling:
      title: Traefik One
```
A `timestamp.log` file is create in `fc-events-profiling/`:
```
Traefik Two
0	1.238	59	83	config	
1	1.238	61	83	pre_build	
2	2.014	308	1720	files	
3	2.086	415	1720	nav	
4	2.090	416	1720	pre_page	
5	2.090	417	1720	page_read_source	
6	2.092	442	1720	page_markdown	
7	2.146	666	1720	page_content	
8	2.146	665	1720	pre_page	contributing/advocating/ 
id time malloc mallocmax event [page]
```

## Graph profil(s) memory with `mathplot`

⚠️ Alpha of Alpha version 😉

```
python3 -m mkdocs_plugin_fc_events_chart logfileone.log [logfiletwo.log]
```
