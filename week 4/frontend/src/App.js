import React, { useState } from 'react';

function App() {
  const [getParam, setGetParam] = useState('');
  const [postParam, setPostParam] = useState('');
  const [postBody, setPostBody] = useState('');
  const [responseMsg, setResponseMsg] = useState('等待指令');
  const handleGetRequest = async () => {
    try {
      // fetch 是浏览器自带的发送网络请求的神器
      const response = await fetch(`http://127.0.0.1:5000/api/test_get?param1=${getParam}`);
      const data = await response.json();
      setResponseMsg(`GET 成功: ${data.result}`);
    } catch (error) {
      setResponseMsg('GET 失败: 网络中断 检查Flask是否运行');
    }
  };

  // ----------------------------------------
  // 任务 2: 发送 POST 请求
  // ----------------------------------------
  const handlePostRequest = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/test_post?my_param=${postParam}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ my_body: postBody }), 
      });
      const data = await response.json();
      setResponseMsg(`POST 成功: ${data.result}`);
    } catch (error) {
      setResponseMsg('POST 失败: 网络中断 检查Flask是否运行');
    }
  };

  return (
    <div style={{ padding: '40px', fontFamily: 'Arial, sans-serif', maxWidth: '600px', margin: '0 auto' }}>
      <h2>控制台</h2>
      
      <div style={{ padding: '20px', backgroundColor: '#000000', color: '#2600ff', borderRadius: '6px', marginBottom: '32px' }}>
        <strong>服务器回传信息：</strong>
        <p>{responseMsg}</p>
      </div>

      <hr />

      <div style={{ margin: '30px 0' }}>
        <h3>1. 测试 GET 请求</h3>
        <input 
          type="text" 
          placeholder="输入" 
          value={getParam}
          onChange={(e) => setGetParam(e.target.value)}
          style={{ padding: '8px', marginRight: '10px', width: '200px' }}
        />
        <button onClick={handleGetRequest} style={{ padding: '8px 16px', cursor: 'pointer' }}>
          发送 GET 信号
        </button>
      </div>

      <hr />

      <div style={{ margin: '30px 0' }}>
        <h3>2. 测试 POST 请求</h3>
        <div style={{ marginBottom: '10px' }}>
          <input 
            type="text" 
            placeholder="输入 URL" 
            value={postParam}
            onChange={(e) => setPostParam(e.target.value)}
            style={{ padding: '8px', marginRight: '10px', width: '250px' }}
          />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <input 
            type="text" 
            placeholder="输入 Body" 
            value={postBody}
            onChange={(e) => setPostBody(e.target.value)}
            style={{ padding: '8px', marginRight: '10px', width: '250px' }}
          />
        </div>
        <button onClick={handlePostRequest} style={{ padding: '8px 16px', cursor: 'pointer' }}>
          发送 POST 信号包
        </button>
      </div>
    </div>
  );
}

export default App;