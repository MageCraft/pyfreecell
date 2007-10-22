# Create your views here.
from django.http import HttpResponse

g_count = 0
deck_seed_map = {}
data_fn = 'freecell/small-list'
data_fh = None
MAX_SEED=32000

def read_deck_by_seed(seed):
    assert (seed >= 0 and seed <= MAX_SEED)
    assert data_fh
    data_fh.seek(seed*52)
    s = data_fh.read(52)
    deck = [ord(i) for i in s]
    assert len(deck) == 52
    return deck


def index(request):
    global g_count
    g_count += 1
    return HttpResponse('You are here, %d' % (g_count,))

def detail(request, seed):
    global data_fh, deck_seed_map
    if data_fh is None:
        #first time 
        data_fh = open(data_fn, 'r')
    seed = int(seed)
    assert (seed >= 0 and seed <= MAX_SEED)
    deck = []
    if deck_seed_map.has_key(seed):
        print 'already have such deck'
        deck = deck_seed_map[seed]
    else:
        #read it from file
        deck = read_deck_by_seed(seed)
        deck_seed_map[seed] = deck
    return HttpResponse('Deck by %d is %s' % (seed, str(deck)))
