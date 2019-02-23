// Powered by Infostretch 

timestamps {

node () {

	stage ('azure-blob-sidecar - Checkout') {
 	 checkout([$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[credentialsId: '75b43bf6-74d1-4ca2-9cda-3490a5a616ee', url: 'https://git.frank-loeppert.com/floeppert/k8s-backup-azure-blob.git']]]) 
	}
	stage ('azure-blob-sidecar - Build') {
 	
environment {
        RegPassword     = credentials('RegistryPassword')
    }

sh """ 
docker build --no-cache --tag k8s-backup-azure-blob:latest . 
 """		// Shell build step
sh """ 
docker tag k8s-backup-azure-blob:latest hub.frank-loeppert.com/k8s-backup-azure-blob:latest 
 """		// Shell build step
sh """ 
docker login -u hub -p $RegPassword hub.frank-loeppert.com 
 """		// Shell build step
sh """ 
docker push hub.frank-loeppert.com/k8s-backup-azure-blob:latest 
 """		// Shell build step
sh """ 
docker image rm k8s-backup-azure-blob -f 
 """		// Shell build step
sh """ 
docker image rm hub.frank-loeppert.com/k8s-backup-azure-blob:latest -f 
 """ 
	}
}
}