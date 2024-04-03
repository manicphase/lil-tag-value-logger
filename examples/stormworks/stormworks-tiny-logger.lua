-- Tick function that will be executed every logic tick
ticks = 0
session_id = 0

function httpReply(port, request_body, response_body)
	session_id = response_body
end

function onTick()
	ticks = ticks + 1
	if ticks == 60 then
		ticks = 0
		async.httpGet(8000, "/add?value=" .. input.getNumber(1) .. "&tag=" .. property.getText("tag"))
	end
	output.setNumber(1, session_id)		-- Write a number to the script's composite output
end

