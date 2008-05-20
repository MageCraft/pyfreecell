#ifndef __TEST_STRING_H__
#define __TEST_STRING_H__

class String
{
    public:
	String();
	String(const char* str);
	String(const String& other);
	virtual ~String();

	String & operator=(const String& other);
	String & operator=(const char* str);
	bool operator==(const String& other);
	bool operator!=(const String& other);

	const char& operator[](unsigned int index) const;
	char& operator[](unsigned int index);

	const char* c_str() const;


    private:
	char* m_data;

};

#endif /*__TEST_STRING_H__*/
