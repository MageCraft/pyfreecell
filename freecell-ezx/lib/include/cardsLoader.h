#ifndef __GET_CARDS_H__
#define __GET_CARDS_H__

#define MAX_CARDS 52

class QImage;
class QPixmap;
class CardsLoader
{
  public:
    CardsLoader();
    ~CardsLoader();

    bool init();
    QPixmap* loadCard(int num);
    QPixmap* loadInvertCard(int num);
};

#endif /*__GET_CARDS_H__*/
