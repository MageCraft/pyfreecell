#include "cardsLoader.h"
#include "bmpdata.h"
#include <qmap.h>
#include <qpixmap.h>
#include <qbitmap.h>
#include <qpainter.h>
#include <stdio.h>

static const int w = 29;
static const int h = 38;
static QPixmap* normal_cards[MAX_CARDS] = {0};
static QPixmap* invert_cards[MAX_CARDS] = {0};
static const QImage* wholeImage;


static QBitmap* mask = NULL;
void init_mask()
{
    //init mask
    mask = new QBitmap(w,h);
    CHECK_PTR(mask);
    QPainter painter;
    painter.begin(mask);
    painter.fillRect(0, 0, mask->width(), mask->height(), QBrush(Qt::color1));

    painter.setPen(Qt::color0);
    //topleft
    painter.drawPoint(0,0);
    painter.drawPoint(0,1);
    painter.drawPoint(1,0);
    //topright
    painter.drawPoint(w-1,0);
    painter.drawPoint(w-2,0);
    painter.drawPoint(w-1,1);
    //bottomleft
    painter.drawPoint(0,h-1);
    painter.drawPoint(1,h-1);
    painter.drawPoint(0,h-2);
    //bottomright
    painter.drawPoint(w-1,h-1);
    painter.drawPoint(w-2,h-1);
    painter.drawPoint(w-1,h-2);

    painter.end();
    
}

QPixmap* invertCards(QPixmap* src)
{
  CHECK_PTR(src);
  QImage image = src->convertToImage();
  ASSERT( !image.isNull() );
  image.invertPixels();
  QPixmap* pixmap = new QPixmap();
  *pixmap = image;
  ASSERT( !pixmap.isNull() );
  return pixmap;
}

QPixmap* invertCards(QImage& src)
{
  CHECK_PTR(src);
  src.invertPixels();
  QPixmap* pixmap = new QPixmap();
  *pixmap = src;
  ASSERT( !pixmap.isNull() );
  return pixmap;
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//
// CardsLoader
//

CardsLoader::CardsLoader() 
{

}

CardsLoader::~CardsLoader() 
{

  for( int i = 0 ; i < MAX_CARDS ; ++i )
  {
      delete normal_cards[i];
      delete invert_cards[i];
  }

}

bool CardsLoader::init() 
{
    /*
  wholeImage = &qembed_findImage("cards");
  if( wholeImage == NULL )
    return false;
    */
  return true;
}


QPixmap* CardsLoader::loadCard(int num)
{
  ASSERT ( num >= 0 && num < MAX_CARDS );
  if( normal_cards[num] != NULL)
      return normal_cards[num];

  /*
  //split wholeImage into small pixmaps at first time
  static const int W = wholeImage->width();
  static const int H = wholeImage->height();
  int x = 0;
  int y = 0;
  init_mask();
  for( int i = 0 ; i < MAX_CARDS ; ++i )
  {

      x = (i / 4) * w;
      y = H - (i % 4+1) * h;

      QPixmap* pixmap = new QPixmap(w, h);

      CHECK_PTR(pixmap);
      QPainter painter;
      painter.begin(pixmap);
      painter.drawImage(0, 0, *wholeImage, x, y, w, h);
      painter.end();

      normal_cards[i] = pixmap;
      invert_cards[i] = invertCards(pixmap);

      normal_cards[i]->setMask(*mask);
      invert_cards[i]->setMask(*mask);
  }

  delete wholeImage;
  delete mask;
  */
  init_mask();
  for( int i = 0 ; i < MAX_CARDS ; ++i )
  {
      char name[10] = {0};
      if( i < 40 ) {
          sprintf(name, "card%02d", i );
      }
      else {
          sprintf(name, "card%02d_1", i );
      }

      QImage* image = qembed_findImage( QString(name) );
      ASSERT( !image->isNull() );

      QPixmap* pixmap = new QPixmap();
      *pixmap = *image;

      ASSERT( !pixmap->isNull() );

      normal_cards[i] = pixmap;
      QImage image2 = image->copy();
      ASSERT( !image2.isNull() );
      invert_cards[i] = invertCards(image2);

      normal_cards[i]->setMask(*mask);
      invert_cards[i]->setMask(*mask);
  }
  delete mask;

  return normal_cards[num];

}

QPixmap* CardsLoader::loadInvertCard(int num)
{
    ASSERT( num >= 0 && num < MAX_CARDS );

    CHECK_PTR(invert_cards[num]);
    return invert_cards[num];
}
