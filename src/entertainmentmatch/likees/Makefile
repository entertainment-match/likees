messages:
	django-admin.py makemessages --all

relative:
	grep --color -R -E "action=\"[a-z]" templates
	grep --color -R -E "href=\"[a-z]" templates

soulmates:
	bash -c "echo -e \"from likees.utils import soulmates\nsoulmates.main()\" | python ../manage.py shell --settings=settings_pro_shell"

title_traductor:
	bash -c "echo -e \"import settings\nfrom likees.utils import title_traductor\ntitle_traductor.main()\" | python ../manage.py shell"

sitemap:
	bash -c "echo -e \"from likees.utils import sitemap\nsitemap.main()\" | python ../manage.py shell --settings=settings_pro_shell"

importer_loader:
	bash -c "echo -e \"from likees.utils import importer, loader\nimporter.main()\nloader.main()\" | python ../manage.py shell --settings=settings_pro_shell"
