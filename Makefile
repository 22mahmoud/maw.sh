# config
SRC 	:= src
DIST 	:= dist
NAME 	:= 'Mahmoud Ashraf'
URL 	:= 'https://mahmoudashraf.dev'

gen:
	[ -d $(DIST) ] || mkdir $(DIST)
	./ssg5/ssg5 $(SRC) $(DIST) $(NAME) $(URL)

watch:
	ls -d $(SRC)/* | entr -d $(MAKE) gen

server:
	python3 -m http.server -d $(DIST)

dev:
	$(MAKE) clean -j2 watch server

clean:
	rm -rf dist

.PHONY : gen clean watch server dev
