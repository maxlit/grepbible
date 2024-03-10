gbib -c "-- Look Up a Single Verse"
gbib -c "John 3:11"

echo "-- Compare Verses in Different Translations"
gbib -v kj,pl -c "Romans 8:20"

echo "-- Lookup a Chapter"
gbib -c 'Psalms 117'

echo "-- Show a Range of Verses"
gbib -c "Gen 41:29-30"

echo "-- Fetch Multiple Disjoint Verses"
gbib -c "Genesis 1:1,3"

echo "-- Compare different versions"
gbib -c 'Gen 41:29-30' -v kj,vg -i

echo "-- random quote"
gbib -r

echo "-- random quote i different languages"
gbib -r -v kj,de,vg

echo "parse a quote"
gbib -c "Gen 41:29-30" --parse