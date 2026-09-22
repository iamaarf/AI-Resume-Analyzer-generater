const API_BASE_URL =
  "https://ai-resume-analyzer-generater.onrender.com";
  


export async function generateResume(
  resumeData
) {
  const response = await fetch(
    `${API_BASE_URL}/build-resume`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(
        resumeData
      ),
    }
  );

  const data =
    await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
      "Unable to generate resume."
    );
  }

  return data;
}