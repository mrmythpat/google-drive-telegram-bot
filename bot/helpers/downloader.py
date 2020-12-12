import os
import wget
import glob
import youtube_dl
from pySmartDL import SmartDL
from urllib.error import HTTPError
from youtube_dl import DownloadError
from bot import DOWNLOAD_DIRECTORY, LOGGER
import torrent_client as lt
import time

def download_file(url, dl_path):
  try:
    dl = SmartDL(url, dl_path, progress_bar=True)
    LOGGER.info(f'Downloading: {url} in {dl_path}')
    dl.start()
    return True, dl.get_dest()
  except HTTPError as error:
    return False, error
  except Exception as error:
    try:
      filename = wget.download(url, dl_path)
      return True, os.path.join(f"{DOWNLOAD_DIRECTORY}/{filename}")
    except HTTPError:
      return False, error


def utube_dl(link):
  ytdl_opts = {
    'outtmpl' : os.path.join(DOWNLOAD_DIRECTORY, '%(title)s'),
    'noplaylist' : True,
    'logger': LOGGER,
    'format': 'bestvideo+bestaudio/best',
    'geo_bypass_country': 'IN'
  }
  with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
    try:
      meta = ytdl.extract_info(link, download=True)
    except DownloadError as e:
      return False, str(e)
    for path in glob.glob(os.path.join(DOWNLOAD_DIRECTORY, '*')):
      if path.endswith(('.avi', '.mov', '.flv', '.wmv', '.3gp','.mpeg', '.webm', '.mp4', '.mkv')) and \
          path.startswith(ytdl.prepare_filename(meta)):
        return True, path
    return False, 'Something went wrong! No video file exists on server.'

def download_file(url, dl_path):
 try:
 ses = lt.session()
 ses.listen_on(6881, 6891)
 params = {
     'save_path': 'DOWNLOAD_DIRECTORY',
     'storage_mode': lt.storage_mode_t(2),
     'paused': False,
     'auto_managed': True,
     'duplicate_is_error': True}
 link = "MAGNET_LINK_HERE"
 handle = lt.add_magnet_uri(ses, link, params)
 ses.start_dht()

 print 'downloading metadata...'
 while (not handle.has_metadata()):
     time.sleep(1)
 print 'got metadata, starting torrent download...'
 while (handle.status().state != lt.torrent_status.seeding):
     s = handle.status()
     state_str = ['queued', 'checking', 'downloading metadata', \
             'downloading', 'finished', 'seeding', 'allocating']
     print '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
             (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
             s.num_peers, state_str[s.state])
     time.sleep(5)
 except HTTPError as error:
    return False, error

