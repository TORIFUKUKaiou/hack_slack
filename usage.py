from operator import attrgetter
from prettytable import PrettyTable
import humanize
import itertools
from client import create_slack_client


class Usage:
  def __init__(self, name):
    self.name = name
    self.count = 0
    self.size = 0

  def add_size(self, size):
    self.count += 1
    self.size += size

  def humanized_size(self):
    return humanize.naturalsize(usage.size)


if __name__ == '__main__':
  slack_client = create_slack_client()
  members = slack_client.api_call('users.list')['members']
  usage_list = []

  for member in members:
    usage = Usage(member['name'])

    for page in itertools.count(1):
      files = slack_client.api_call(
        'files.list', user=member['id'], page=page)['files']

      if not files:
        break

      for file in files:
        usage.add_size(file['size'])

    usage_list.append(usage)

  usage_list.sort(key=attrgetter('size'), reverse=True)

  table = PrettyTable(['username', 'usage', 'count'])
  table.align = 'r'

  for usage in usage_list:
    table.add_row([usage.name, usage.humanized_size(), usage.count])

  print(table)
