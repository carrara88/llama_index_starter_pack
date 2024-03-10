export type ResponseSources = {
  text: string;
  doc_id: string;
  start: number;
  end: number;
  similarity: number;
};

const login = async (username: string, password:string=""): Promise<any> => {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);

  const requestURL = new URL('http://localhost:5601/login');
  const response = await fetch(requestURL, { mode: 'cors', body: formData, method: 'POST' });
  if (!response.ok) {
    return { text: 'Error on login' };
  }

  const jsonResponse = (await response.json());
  return jsonResponse;
};

export default login;
