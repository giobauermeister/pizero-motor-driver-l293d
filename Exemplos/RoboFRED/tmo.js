(function() {
	window.Main = {};
	Main.Page = (function() {
		var mosq = null;
		function Page() {
			var _this = this;
			mosq = new Mosquitto();

			$('#connect-button').click(function() {
				return _this.connect();
			});
			$('#disconnect-button').click(function() {
				return _this.disconnect();
			});
			
			//ações do robô
			$('#frente').click(function() {
				var payload = "F";  
				var TopicPublish = "RaspZeroWRobo";
				mosq.publish(TopicPublish, payload, 0);
			});

			$('#direita').click(function() {
				var payload = "D";  
				var TopicPublish = "RaspZeroWRobo";
				mosq.publish(TopicPublish, payload, 0);
			});
			
			$('#esquerda').click(function() {
				var payload = "E";  
				var TopicPublish = "RaspZeroWRobo";				
				mosq.publish(TopicPublish, payload, 0);
			});
			
			$('#re').click(function() {
				var payload = "R";  
				var TopicPublish = "RaspZeroWRobo";
				mosq.publish(TopicPublish, payload, 0);
			});

                        $('#parar').click(function() {
				var payload = "P";  
				var TopicPublish = "RaspZeroWRobo";
				mosq.publish(TopicPublish, payload, 0);
			});
			

			mosq.onconnect = function(rc){
				var p = document.createElement("p");
				p.innerHTML = "Conectado ao Broker!";
				$("#debug").append(p);
			};
			mosq.ondisconnect = function(rc){
				var p = document.createElement("p");
				var url = "ws://iot.eclipse.org/ws";
				
				p.innerHTML = "A conexão com o broker foi perdida";
				$("#debug").append(p);				
				mosq.connect(url);
			};
			mosq.onmessage = function(topic, payload, qos){
				var p1 = document.createElement("p1");
				var p2 = document.createElement("p2");
				var payload_util = payload.substring(0, 3);
			};
		}
		Page.prototype.connect = function(){
			var url = "ws://iot.eclipse.org/ws";
			mosq.connect(url);
		};
		Page.prototype.disconnect = function(){
			mosq.disconnect();
		};
		Page.prototype.subscribe = function(){
			var topic = $('#sub-topic-text')[0].value;
			mosq.subscribe(topic, 0);
		};
		Page.prototype.unsubscribe = function(){
			var topic = $('#sub-topic-text')[0].value;
			mosq.unsubscribe(topic);
		};
		
		return Page;
	})();
	$(function(){
		return Main.controller = new Main.Page;
	});
}).call(this);

