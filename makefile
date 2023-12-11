git:
	git add .
	git commit -m "$m"
	git push -u origin Dev
	git checkout Qa
	git merge Dev
	git push -u origin Qa
