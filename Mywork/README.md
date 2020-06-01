# Infra WIFI Indoor loalization: Multiverse with 0 speed

- Improvement exist paper 'Multiverse: Mobility pattern understanding improves localization accuracy'
- 건물내에 존재하는 WiFi 서버에 들어오는 데이터를 이용하여 유저의 실내 위치를 추적하는 기술이다.
- 기존연구는 사람이 한자리에 가만히 있는것에 대한 한계점이 있었다.
- 사람들이 건물안에서 누군가와 이야기를 하거나 휴대폰을 사용하기위해 멈추거나 하는 등의 행동패턴이 존재하기때문에 기능을 추가하게 되었다.

- 참고한 논문설명 <https://github.com/Sunny8747/WIFI_Indoor_localization/tree/master/Previous_paper>

- My Code <https://github.com/Sunny8747/WIFI_Indoor_localization/blob/master/Mywork/Multiverse_with_0speed/matrix_graph_build.py>

- Report <https://github.com/Sunny8747/WIFI_Indoor_localization/blob/master/Mywork/Multiverse_with_0speed/Multiverse_with_0speed.pdf>

<hr/>

## Code description

```python
  #processing black white image to node grid for graph building
  def Image_processing():

  #get node number with location of node
  def node_finder(x,y):

  #find probable location of user with server wifi data (ap_name, rssi_value, offset)
  #offset defines sensitive of wifi estimation
  def probable_location(ap_name, rssi_value, offset):

  #bulding path tree with data to grided image
  def path_tree_constructor():

  #checking difference with next node and prev node
  #this step discard impossible speed of user (teleporting)
  def point_diff_check():
```

## Data sets

- pre_finger : server crawl data
- off_finger1 : result of **'off_fingerprint_map_step2'** after doing job need delete useless space(before or after epochTime of mobile application coordinate data)
- off_finger2 : result of **'off_fingerprint_map_step2'**

- If you want to add finger data to previous one then add to off_finger2 is fine
  the lastfinger will generate final fingerprint map automatically

- Image Size in mobile

  - x:2310
  - y:922

- Image Size in bmp

  - x:751
  - y:300

- Coord Transformation Factor
  - x:0.32511
  - y:0.32538

<hr/>
