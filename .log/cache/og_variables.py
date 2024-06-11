# ask user for extended input and if is Yes than add to memcached2_open_graph
if input('Do you want to enter extended OpenGraph variables? (y/n): ') == 'y':
  path += f'y/'
  get_input_from_dict(OG_EXTENDED_LIST)
  # check if og:type is selected and if it is music than add OG_EXTENDED_LIST_MUSIC to memcached2_open_graph
  if OGValidation().isItMusic(OG_LIST):
    get_input_from_dict(OG_EXTENDED_LIST_MUSIC)
    memcached2_open_graph.append(OG_EXTENDED_LIST_MUSIC)
else:
  path += f'n/'
  filename = 'shorten__memcached2_open_graph'
  save_and_exit(memcached2_open_graph)