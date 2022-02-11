def users_mannual():
    print("""

    input parameters: 
    fab deploy  
    	--no-migrate  		@> to skip migration in the master; default=True
    	--no-dependencies	@> to skip dependencies in every server; default=True		; works only for --django or --deploy_together 
    	--collectstatic		@> to collect static files; default=False					; works only for --django or --deploy_together
    	--django 			@> to deploy django application; default=False				;
    	--react				@> to deploy react applicatio; default=False				;
    	--deploy_together	@> this will deploy both together. django in preference 	; default=False ;
    	--django_branch		@> to mention which branch of django application have to get deployed; default='master';
    	--react_branch		@> to mention which branch of django application have to get deployed; default='master'; 
    	--help				@> to display user manual and exit();
    """);


