const insertDocument = async (file: File, authKey='') => {

  const formData = new FormData();
  formData.append('llm_type', 'cloud'); // or 'local'
  formData.append('file', file);
  formData.append('filename_as_doc_id', 'true');
  formData.append('auth_key', authKey);

  const response = await fetch('http://localhost:5601/insert_document', {
    mode: 'cors',
    method: 'POST',
    body: formData,
  });

  const jsonResponse = (await response.json());
  return jsonResponse;
};

export default insertDocument;
