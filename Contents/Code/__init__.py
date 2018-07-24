import hashlib, inspect, os, datetime

STATIC_POSTER = 'static_poster.png'
STATIC_BACKGROUND = 'static_background.png'

def Start():
  pass
  
def ValidatePrefs():
  pass
  
def processTrailerMovies(metadata, media):
  part = media.items[0].parts[0]
  (root_file, ext) = os.path.splitext(os.path.basename(part.file))
  
  prefix = ''
  if Prefs['trailer_prefix']:
    prefix = Prefs['trailer_prefix']
    
  suffix = ''
  if Prefs['trailer_suffix']:
    suffix = Prefs['trailer_suffix']
  
  metadata.title = prefix + root_file + suffix
  
  if Prefs['filemdate']:
    mod_time = os.path.getmtime(part.file)
    date = datetime.date.fromtimestamp(mod_time)
    metadata.year = date.year
    metadata.originally_available_at = Datetime.ParseDate(str(date)).date()
  else:
    metadata.year = None
    metadata.originally_available_at = None

  if Prefs['static_poster']:
    if Prefs['static_poster_path']:
      data = Core.storage.load(Prefs['static_poster_path'])
    else:
      data = Core.storage.load(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), STATIC_POSTER))
    media_hash = hashlib.md5(data).hexdigest()

    tmp = []
    for index in metadata.posters:
      tmp.append(index)
    for index in tmp:
      if index != media_hash:
        del metadata.posters[index]
      
    if media_hash not in metadata.posters:
      metadata.posters[media_hash] = Proxy.Media(data, sort_order=1)
      Log('[TRAILER] Static poster added for %s' % root_file)
  
  if Prefs['static_background']:  
    if Prefs['static_background_path']:
      data = Core.storage.load(Prefs['static_background_path'])
    else:
      data = Core.storage.load(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), STATIC_BACKGROUND))
    media_hash = hashlib.md5(data).hexdigest()

    tmp = []
    for index in metadata.art:
      tmp.append(index)
    for index in tmp:
      if index != media_hash:
        del metadata.art[index]
      
    if media_hash not in metadata.art:
      metadata.art[media_hash] = Proxy.Media(data, sort_order=1)
      Log('[TRAILER] Static background added for %s' % root_file)
      
class LocalTrailerAgent(Agent.Movies):
  name = 'Local Trailer'
  languages = [Locale.Language.NoLanguage]
  primary_provider = True
  accepts_from = ['com.plexapp.agents.localmedia', 'com.plexapp.agents.youtube']

  def search(self, results, media, lang):
    Log('[TRAILER] Searching for %s' % media.name)
    results.Append(MetadataSearchResult(id = media.id, name = media.name, year = None, score = 100, lang = lang))

  def update(self, metadata, media, lang):
    processTrailerMovies(metadata, media)