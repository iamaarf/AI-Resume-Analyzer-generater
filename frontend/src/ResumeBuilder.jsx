import { useState } from "react";
import "./ResumeBuilder.css";
import {
  Document,
  Page,
  Text,
  View,
  StyleSheet,
  PDFDownloadLink,
} from "@react-pdf/renderer";
import {
  generateResume
} from "./resume_builder_api";
const pdfStyles = StyleSheet.create({
  page: {
    padding: 36,
    fontSize: 10,
    fontFamily: "Helvetica",
    color: "#222222",
  },

  name: {
    fontSize: 22,
    fontWeight: "bold",
    marginBottom: 4,
  },

  targetRole: {
    fontSize: 12,
    marginBottom: 8,
  },

  contact: {
    fontSize: 9,
    marginBottom: 3,
  },

  section: {
    marginTop: 14,
  },

  sectionTitle: {
    fontSize: 12,
    fontWeight: "bold",
    marginBottom: 6,
    borderBottomWidth: 1,
    borderBottomColor: "#cccccc",
    paddingBottom: 3,
  },

  text: {
    fontSize: 10,
    lineHeight: 1.45,
    marginBottom: 4,
  },

  bullet: {
    fontSize: 10,
    lineHeight: 1.4,
    marginBottom: 3,
    paddingLeft: 8,
  },

  experienceTitle: {
    fontSize: 11,
    fontWeight: "bold",
    marginBottom: 2,
  },

  experienceMeta: {
    fontSize: 9,
    marginBottom: 5,
  },

  projectName: {
    fontSize: 11,
    fontWeight: "bold",
    marginBottom: 3,
  },

  technology: {
    fontSize: 9,
    marginBottom: 4,
  },
});

function ResumePDF({ resume }) {
  return (
    <Document>
      <Page size="A4" style={pdfStyles.page}>

        <Text style={pdfStyles.name}>
          {resume.name || ""}
        </Text>

        <Text style={pdfStyles.targetRole}>
          {resume.targetRole || ""}
        </Text>

        <Text style={pdfStyles.contact}>
          {resume.email || ""} | {resume.phone || ""}
        </Text>

        <Text style={pdfStyles.contact}>
          {resume.location || ""}
        </Text>

        {resume.linkedin ? (
          <Text style={pdfStyles.contact}>
            {resume.linkedin}
          </Text>
        ) : null}

        {resume.professional_summary ? (
          <View style={pdfStyles.section}>
            <Text style={pdfStyles.sectionTitle}>
              Professional Summary
            </Text>

            <Text style={pdfStyles.text}>
              {resume.professional_summary}
            </Text>
          </View>
        ) : null}

        {resume.skills?.length > 0 ? (
          <View style={pdfStyles.section}>
            <Text style={pdfStyles.sectionTitle}>
              Skills
            </Text>

            {resume.skills.map((skill, index) => (
              <Text
                key={index}
                style={pdfStyles.bullet}
              >
                • {skill}
              </Text>
            ))}
          </View>
        ) : null}

        {resume.work_experience?.length > 0 ? (
          <View style={pdfStyles.section}>
            <Text style={pdfStyles.sectionTitle}>
              Work Experience
            </Text>

            {resume.work_experience.map(
              (experience, index) => (
                <View key={index}>
                  <Text style={pdfStyles.experienceTitle}>
                    {experience.title || ""}
                  </Text>

                  <Text style={pdfStyles.experienceMeta}>
                    {experience.company || ""}
                    {" | "}
                    {experience.dates || ""}
                  </Text>

                  {experience.responsibilities?.map(
                    (item, bulletIndex) => (
                      <Text
                        key={bulletIndex}
                        style={pdfStyles.bullet}
                      >
                        • {item}
                      </Text>
                    )
                  )}
                </View>
              )
            )}
          </View>
        ) : null}

        {resume.education?.length > 0 ? (
          <View style={pdfStyles.section}>
            <Text style={pdfStyles.sectionTitle}>
              Education
            </Text>

            {resume.education.map(
              (education, index) => (
                <View key={index}>
                  <Text style={pdfStyles.experienceTitle}>
                    {education.degree || ""}
                  </Text>

                  <Text style={pdfStyles.text}>
                    {education.specialization || ""}
                  </Text>

                  <Text style={pdfStyles.experienceMeta}>
                    {education.institution || ""}
                    {" | "}
                    {education.year || ""}
                  </Text>
                </View>
              )
            )}
          </View>
        ) : null}

        {resume.projects?.length > 0 ? (
          <View style={pdfStyles.section}>
            <Text style={pdfStyles.sectionTitle}>
              Projects
            </Text>

            {resume.projects.map(
              (project, index) => (
                <View key={index}>
                  <Text style={pdfStyles.projectName}>
                    {project.name || project.title || ""}
                  </Text>

                  {project.technologies ? (
                    <Text style={pdfStyles.technology}>
                      {Array.isArray(project.technologies)
                        ? project.technologies.join(" • ")
                        : project.technologies}
                    </Text>
                  ) : null}

                  {project.description ? (
                    <Text style={pdfStyles.text}>
                      {project.description}
                    </Text>
                  ) : null}

                  {project.responsibilities?.map(
                    (item, bulletIndex) => (
                      <Text
                        key={bulletIndex}
                        style={pdfStyles.bullet}
                      >
                        • {item}
                      </Text>
                    )
                  )}
                </View>
              )
            )}
          </View>
        ) : null}

        {resume.certifications?.length > 0 ? (
          <View style={pdfStyles.section}>
            <Text style={pdfStyles.sectionTitle}>
              Certifications
            </Text>

            {resume.certifications.map(
              (certification, index) => (
                <Text
                  key={index}
                  style={pdfStyles.bullet}
                >
                  • {certification.name || ""}
                  {" — "}
                  {certification.organization || ""}
                  {" ("}
                  {certification.date || ""}
                  {")"}
                </Text>
              )
            )}
          </View>
        ) : null}

        {resume.languages?.length > 0 ? (
          <View style={pdfStyles.section}>
            <Text style={pdfStyles.sectionTitle}>
              Languages
            </Text>

            <Text style={pdfStyles.text}>
              {resume.languages.join(" • ")}
            </Text>
          </View>
        ) : null}

      </Page>
    </Document>
  );
}

function ResumeBuilder() {

  const [resume, setResume] = useState({
    name: "",
    email: "",
    phone: "",
    location: "",
    linkedin: "",

    targetRole: "",
    jobDescription: "",

    experiences: [
      {
        jobTitle: "",
        company: "",
        startDate: "",
        endDate: "",
        description: "",
      },
    ],

    projects: [
      {
        name: "",
        technologies: "",
        description: "",
      },
    ],

    skills: "",

    education: [
      {
        degree: "",
        specialization: "",
        institution: "",
        year: "",
      },
    ],

    certifications: [
      {
        name: "",
        organization: "",
        date: "",
      },
    ],
  });


  const [generated, setGenerated] =
    useState(false);

  const [generatedResume, setGeneratedResume] =
    useState(null);

  const [isGenerating, setIsGenerating] =
    useState(false);

  const [generationError, setGenerationError] =
    useState("");


  /* ================================
     BASIC FIELD CHANGE
  ================================= */

  const handleChange = (event) => {

    const { name, value } = event.target;

    setResume((previous) => ({
      ...previous,
      [name]: value,
    }));

    setGenerated(false);
    setGeneratedResume(null);
    setGenerationError("");
  };


  /* ================================
     EXPERIENCE
  ================================= */

  const handleExperienceChange = (
    index,
    field,
    value
  ) => {

    setResume((previous) => {

      const experiences = [
        ...previous.experiences,
      ];

      experiences[index] = {
        ...experiences[index],
        [field]: value,
      };

      return {
        ...previous,
        experiences,
      };
    });

    setGenerated(false);
    setGeneratedResume(null);
  };


  const addExperience = () => {

    setResume((previous) => ({
      ...previous,

      experiences: [
        ...previous.experiences,

        {
          jobTitle: "",
          company: "",
          startDate: "",
          endDate: "",
          description: "",
        },
      ],
    }));
  };


  const removeExperience = (index) => {

    setResume((previous) => {

      const experiences =
        previous.experiences.filter(
          (_, itemIndex) =>
            itemIndex !== index
        );

      return {
        ...previous,
        experiences:
          experiences.length > 0
            ? experiences
            : [
                {
                  jobTitle: "",
                  company: "",
                  startDate: "",
                  endDate: "",
                  description: "",
                },
              ],
      };
    });

    setGenerated(false);
    setGeneratedResume(null);
  };


  /* ================================
     PROJECTS
  ================================= */

  const handleProjectChange = (
    index,
    field,
    value
  ) => {

    setResume((previous) => {

      const projects = [
        ...previous.projects,
      ];

      projects[index] = {
        ...projects[index],
        [field]: value,
      };

      return {
        ...previous,
        projects,
      };
    });

    setGenerated(false);
    setGeneratedResume(null);
  };


  const addProject = () => {

    setResume((previous) => ({
      ...previous,

      projects: [
        ...previous.projects,

        {
          name: "",
          technologies: "",
          description: "",
        },
      ],
    }));
  };


  const removeProject = (index) => {

    setResume((previous) => {

      const projects =
        previous.projects.filter(
          (_, itemIndex) =>
            itemIndex !== index
        );

      return {
        ...previous,
        projects:
          projects.length > 0
            ? projects
            : [
                {
                  name: "",
                  technologies: "",
                  description: "",
                },
              ],
      };
    });

    setGenerated(false);
    setGeneratedResume(null);
  };


  /* ================================
     EDUCATION
  ================================= */

  const handleEducationChange = (
    index,
    field,
    value
  ) => {

    setResume((previous) => {

      const education = [
        ...previous.education,
      ];

      education[index] = {
        ...education[index],
        [field]: value,
      };

      return {
        ...previous,
        education,
      };
    });

    setGenerated(false);
    setGeneratedResume(null);
  };


  const addEducation = () => {

    setResume((previous) => ({
      ...previous,

      education: [
        ...previous.education,

        {
          degree: "",
          specialization: "",
          institution: "",
          year: "",
        },
      ],
    }));
  };


  const removeEducation = (index) => {

    setResume((previous) => {

      const education =
        previous.education.filter(
          (_, itemIndex) =>
            itemIndex !== index
        );

      return {
        ...previous,
        education:
          education.length > 0
            ? education
            : [
                {
                  degree: "",
                  specialization: "",
                  institution: "",
                  year: "",
                },
              ],
      };
    });

    setGenerated(false);
    setGeneratedResume(null);
  };


  /* ================================
     CERTIFICATIONS
  ================================= */

  const handleCertificationChange = (
    index,
    field,
    value
  ) => {

    setResume((previous) => {

      const certifications = [
        ...previous.certifications,
      ];

      certifications[index] = {
        ...certifications[index],
        [field]: value,
      };

      return {
        ...previous,
        certifications,
      };
    });

    setGenerated(false);
    setGeneratedResume(null);
  };


  const addCertification = () => {

    setResume((previous) => ({
      ...previous,

      certifications: [
        ...previous.certifications,

        {
          name: "",
          organization: "",
          date: "",
        },
      ],
    }));
  };


  const removeCertification = (index) => {

    setResume((previous) => {

      const certifications =
        previous.certifications.filter(
          (_, itemIndex) =>
            itemIndex !== index
        );

      return {
        ...previous,
        certifications:
          certifications.length > 0
            ? certifications
            : [
                {
                  name: "",
                  organization: "",
                  date: "",
                },
              ],
      };
    });

    setGenerated(false);
    setGeneratedResume(null);
  };


  /* ================================
     GENERATE RESUME
  ================================= */

  const handleGenerateResume = async () => {

    setIsGenerating(true);
    setGenerated(false);
    setGeneratedResume(null);
    setGenerationError("");

    try {

      const result =
        await generateResume(resume);

      setGeneratedResume(
        result.resume
      );

      setGenerated(true);

    } catch (error) {

      console.error(
        "Resume generation error:",
        error
      );

      setGenerationError(
        error.message ||
        "Unable to generate resume."
      );

    } finally {

      setIsGenerating(false);
    }
  };


  /* ================================
     RENDER
  ================================= */

  return (
    <div className="resume-builder-page">

      {/* PAGE HEADER */}

      <div className="resume-builder-header">

        <div className="resume-builder-badge">
          AI RESUME BUILDER
        </div>

        <h1>
          Build a Job-Ready Resume
        </h1>

        <p>
          Create a professional, ATS-friendly resume
          tailored to your target job.
        </p>

      </div>


      <div className="resume-builder-layout">


        {/* =====================================================
            LEFT SIDE - FORM
        ====================================================== */}

        <section className="resume-builder-form-card">


          {/* =================================================
              1. PERSONAL INFORMATION
          ================================================== */}

          <div className="resume-builder-section-title">

            <h2>
              1. Personal Information
            </h2>

            <p>
              Enter your basic professional contact details.
            </p>

          </div>


          <div className="resume-builder-grid">


            <div className="resume-builder-field">

              <label>
                Full Name
              </label>

              <input
                name="name"
                value={resume.name}
                onChange={handleChange}
                placeholder="Your full name"
              />

            </div>


            <div className="resume-builder-field">

              <label>
                Email
              </label>

              <input
                name="email"
                type="email"
                value={resume.email}
                onChange={handleChange}
                placeholder="you@example.com"
              />

            </div>


            <div className="resume-builder-field">

              <label>
                Phone
              </label>

              <input
                name="phone"
                value={resume.phone}
                onChange={handleChange}
                placeholder="+91 XXXXX XXXXX"
              />

            </div>


            <div className="resume-builder-field">

              <label>
                Location
              </label>

              <input
                name="location"
                value={resume.location}
                onChange={handleChange}
                placeholder="City, State, Country"
              />

            </div>


            <div className="resume-builder-field resume-builder-full">

              <label>
                LinkedIn Profile
              </label>

              <input
                name="linkedin"
                value={resume.linkedin}
                onChange={handleChange}
                placeholder="https://linkedin.com/in/your-profile"
              />

            </div>

          </div>


          {/* =================================================
              2. TARGET JOB
          ================================================== */}

          <div className="resume-builder-section-title">

            <h2>
              2. Target Job
            </h2>

            <p>
              Tell ResumeAI what position you are applying for.
            </p>

          </div>


          <div className="resume-builder-field">

            <label>
              Target Job / Position
            </label>

            <input
              name="targetRole"
              value={resume.targetRole}
              onChange={handleChange}
              placeholder="e.g. Business Analyst"
            />

          </div>


          {/* =================================================
              3. JOB DESCRIPTION
          ================================================== */}

          <div className="resume-builder-section-title">

            <h2>
              3. Job Description
            </h2>

            <p>
              Paste the job description so ResumeAI can
              tailor your resume to the specific role.
            </p>

          </div>


          <div className="resume-builder-field">

            <label>
              Job Description
            </label>

            <textarea
              name="jobDescription"
              value={resume.jobDescription}
              onChange={handleChange}
              placeholder={
                "Paste the job description here...\n\n" +
                "Example:\n" +
                "We are looking for a Business Analyst with experience " +
                "in Excel, Power BI, data analysis and reporting..."
              }
              rows="9"
            />

          </div>


          <div className="resume-builder-info-box">

            <strong>
              How ResumeAI uses this information
            </strong>

            <p>
              ResumeAI will analyze the job requirements
              and use relevant keywords naturally when
              creating your resume.
            </p>

            <p>
              It will not add skills, experience,
              achievements or qualifications that
              you have not provided.
            </p>

          </div>


          {/* =================================================
              4. WORK EXPERIENCE
          ================================================== */}

          <div className="resume-builder-section-title">

            <h2>
              4. Work Experience
            </h2>

            <p>
              Add your experience in your own words.
              You do not need to write professionally.
            </p>

          </div>


          {resume.experiences.map(
            (experience, index) => (

              <div
                className="resume-builder-repeat-box"
                key={index}
              >

                <div className="resume-builder-repeat-header">

                  <strong>
                    Experience {index + 1}
                  </strong>

                  {resume.experiences.length > 1 && (

                    <button
                      type="button"
                      className="resume-builder-remove-button"
                      onClick={() =>
                        removeExperience(index)
                      }
                    >
                      Remove
                    </button>

                  )}

                </div>


                <div className="resume-builder-grid">


                  <div className="resume-builder-field">

                    <label>
                      Job Title
                    </label>

                    <input
                      value={experience.jobTitle}
                      onChange={(event) =>
                        handleExperienceChange(
                          index,
                          "jobTitle",
                          event.target.value
                        )
                      }
                      placeholder="e.g. Business Analyst"
                    />

                  </div>


                  <div className="resume-builder-field">

                    <label>
                      Company
                    </label>

                    <input
                      value={experience.company}
                      onChange={(event) =>
                        handleExperienceChange(
                          index,
                          "company",
                          event.target.value
                        )
                      }
                      placeholder="Company name"
                    />

                  </div>


                  <div className="resume-builder-field">

                    <label>
                      Start Date
                    </label>

                    <input
                      value={experience.startDate}
                      onChange={(event) =>
                        handleExperienceChange(
                          index,
                          "startDate",
                          event.target.value
                        )
                      }
                      placeholder="e.g. Jan 2024"
                    />

                  </div>


                  <div className="resume-builder-field">

                    <label>
                      End Date
                    </label>

                    <input
                      value={experience.endDate}
                      onChange={(event) =>
                        handleExperienceChange(
                          index,
                          "endDate",
                          event.target.value
                        )
                      }
                      placeholder="e.g. Present"
                    />

                  </div>


                  <div className="resume-builder-field resume-builder-full">

                    <label>
                      What did you do?
                    </label>

                    <textarea
                      value={experience.description}
                      onChange={(event) =>
                        handleExperienceChange(
                          index,
                          "description",
                          event.target.value
                        )
                      }
                      placeholder={
                        "Write in simple language.\n\n" +
                        "Example:\n" +
                        "I handled recruitment, interviewed candidates, " +
                        "maintained employee records in Excel and supported HR operations."
                      }
                      rows="7"
                    />

                  </div>

                </div>

              </div>

            )
          )}


          <button
            type="button"
            className="resume-builder-add-button"
            onClick={addExperience}
          >
            + Add Another Experience
          </button>


          {/* =================================================
              5. PROJECTS
          ================================================== */}

          <div className="resume-builder-section-title">

            <h2>
              5. Projects
            </h2>

            <p>
              Add projects that are relevant to your target job.
            </p>

          </div>


          {resume.projects.map(
            (project, index) => (

              <div
                className="resume-builder-repeat-box"
                key={index}
              >

                <div className="resume-builder-repeat-header">

                  <strong>
                    Project {index + 1}
                  </strong>

                  {resume.projects.length > 1 && (

                    <button
                      type="button"
                      className="resume-builder-remove-button"
                      onClick={() =>
                        removeProject(index)
                      }
                    >
                      Remove
                    </button>

                  )}

                </div>


                <div className="resume-builder-grid">


                  <div className="resume-builder-field">

                    <label>
                      Project Name
                    </label>

                    <input
                      value={project.name}
                      onChange={(event) =>
                        handleProjectChange(
                          index,
                          "name",
                          event.target.value
                        )
                      }
                      placeholder="e.g. Sales Dashboard"
                    />

                  </div>


                  <div className="resume-builder-field">

                    <label>
                      Tools / Technologies
                    </label>

                    <input
                      value={project.technologies}
                      onChange={(event) =>
                        handleProjectChange(
                          index,
                          "technologies",
                          event.target.value
                        )
                      }
                      placeholder="e.g. Excel, Power BI"
                    />

                  </div>


                  <div className="resume-builder-field resume-builder-full">

                    <label>
                      Project Details
                    </label>

                    <textarea
                      value={project.description}
                      onChange={(event) =>
                        handleProjectChange(
                          index,
                          "description",
                          event.target.value
                        )
                      }
                      placeholder={
                        "Explain what you did in simple words.\n\n" +
                        "Example:\n" +
                        "I created a Power BI dashboard to analyze sales data " +
                        "and show monthly performance."
                      }
                      rows="6"
                    />

                  </div>

                </div>

              </div>

            )
          )}


          <button
            type="button"
            className="resume-builder-add-button"
            onClick={addProject}
          >
            + Add Another Project
          </button>


          {/* =================================================
              6. SKILLS
          ================================================== */}

          <div className="resume-builder-section-title">

            <h2>
              6. Skills
            </h2>

            <p>
              Add your skills in simple words. Separate multiple
              skills with commas.
            </p>

          </div>


          <div className="resume-builder-field">

            <label>
              Your Skills
            </label>

            <textarea
              name="skills"
              value={resume.skills}
              onChange={handleChange}
              placeholder={
                "Example:\n" +
                "Excel, Power BI, SQL, Data Analysis, Communication"
              }
              rows="5"
            />

          </div>


          {/* =================================================
              7. EDUCATION
          ================================================== */}

          <div className="resume-builder-section-title">

            <h2>
              7. Education
            </h2>

            <p>
              Add your education details.
            </p>

          </div>


          {resume.education.map(
            (education, index) => (

              <div
                className="resume-builder-repeat-box"
                key={index}
              >

                <div className="resume-builder-repeat-header">

                  <strong>
                    Education {index + 1}
                  </strong>

                  {resume.education.length > 1 && (

                    <button
                      type="button"
                      className="resume-builder-remove-button"
                      onClick={() =>
                        removeEducation(index)
                      }
                    >
                      Remove
                    </button>

                  )}

                </div>


                <div className="resume-builder-grid">


                  <div className="resume-builder-field">

                    <label>
                      Degree
                    </label>

                    <input
                      value={education.degree}
                      onChange={(event) =>
                        handleEducationChange(
                          index,
                          "degree",
                          event.target.value
                        )
                      }
                      placeholder="e.g. B.Tech"
                    />

                  </div>


                  <div className="resume-builder-field">

                    <label>
                      Field / Specialization
                    </label>

                    <input
                      value={education.specialization}
                      onChange={(event) =>
                        handleEducationChange(
                          index,
                          "specialization",
                          event.target.value
                        )
                      }
                      placeholder="e.g. Computer Science"
                    />

                  </div>


                  <div className="resume-builder-field">

                    <label>
                      University / College
                    </label>

                    <input
                      value={education.institution}
                      onChange={(event) =>
                        handleEducationChange(
                          index,
                          "institution",
                          event.target.value
                        )
                      }
                      placeholder="Institution name"
                    />

                  </div>


                  <div className="resume-builder-field">

                    <label>
                      Year
                    </label>

                    <input
                      value={education.year}
                      onChange={(event) =>
                        handleEducationChange(
                          index,
                          "year",
                          event.target.value
                        )
                      }
                      placeholder="e.g. 2025"
                    />

                  </div>

                </div>

              </div>

            )
          )}


          <button
            type="button"
            className="resume-builder-add-button"
            onClick={addEducation}
          >
            + Add Another Education
          </button>


          {/* =================================================
              8. CERTIFICATIONS
          ================================================== */}

          <div className="resume-builder-section-title">

            <h2>
              8. Certifications
            </h2>

            <p>
              Add certifications only if you have them.
            </p>

          </div>


          {resume.certifications.map(
            (certification, index) => (

              <div
                className="resume-builder-repeat-box"
                key={index}
              >

                <div className="resume-builder-repeat-header">

                  <strong>
                    Certification {index + 1}
                  </strong>

                  {resume.certifications.length > 1 && (

                    <button
                      type="button"
                      className="resume-builder-remove-button"
                      onClick={() =>
                        removeCertification(index)
                      }
                    >
                      Remove
                    </button>

                  )}

                </div>


                <div className="resume-builder-grid">


                  <div className="resume-builder-field">

                    <label>
                      Certification Name
                    </label>

                    <input
                      value={certification.name}
                      onChange={(event) =>
                        handleCertificationChange(
                          index,
                          "name",
                          event.target.value
                        )
                      }
                      placeholder="e.g. Google Data Analytics"
                    />

                  </div>


                  <div className="resume-builder-field">

                    <label>
                      Issuing Organization
                    </label>

                    <input
                      value={certification.organization}
                      onChange={(event) =>
                        handleCertificationChange(
                          index,
                          "organization",
                          event.target.value
                        )
                      }
                      placeholder="e.g. Google"
                    />

                  </div>


                  <div className="resume-builder-field">

                    <label>
                      Date
                    </label>

                    <input
                      value={certification.date}
                      onChange={(event) =>
                        handleCertificationChange(
                          index,
                          "date",
                          event.target.value
                        )
                      }
                      placeholder="e.g. 2025"
                    />

                  </div>

                </div>

              </div>

            )
          )}


          <button
            type="button"
            className="resume-builder-add-button"
            onClick={addCertification}
          >
            + Add Another Certification
          </button>


          {/* =================================================
              GENERATE BUTTON
          ================================================== */}

          <button
            type="button"
            className="resume-builder-generate-button"
            onClick={handleGenerateResume}
            disabled={isGenerating}
          >

            {isGenerating
              ? "Generating Resume..."
              : "✨ Generate My Resume"}

          </button>


          {generated && generatedResume && (

            <div className="resume-builder-success">

              <strong>
                Resume generated successfully.
              </strong>

              <span>
                ResumeAI has processed your information
                according to the target job.
              </span>

            </div>

          )}


          {generationError && (

            <div className="resume-builder-error">

              <strong>
                Generation failed
              </strong>

              <span>
                {generationError}
              </span>

            </div>

          )}

        </section>


        {/* =====================================================
            RIGHT SIDE - LIVE PREVIEW
        ====================================================== */}

        <section className="resume-builder-preview-card">


          <div className="resume-builder-preview-header">

            <div>

              <h2>
                Live Resume Preview
              </h2>

              <p>
                ATS-friendly single-column structure
              </p>

            </div>


           {generatedResume ? (
  <PDFDownloadLink
    document={
      <ResumePDF
        resume={{
          ...resume,
          ...generatedResume,
        }}
      />
    }
    fileName={`${resume.name || "resume"}.pdf`}
    className="resume-builder-download-button"
  >
    {({ loading }) =>
      loading ? "Preparing PDF..." : "Download PDF"
    }
  </PDFDownloadLink>
) : (
  <button
    type="button"
    className="resume-builder-download-button"
    disabled
  >
    Download PDF
  </button>
)}

          </div>


          <div className="resume-preview">


            {/* HEADER */}

            <div className="resume-preview-top">

              <h1>
                {resume.name || "Your Name"}
              </h1>

              <p>
                {resume.targetRole ||
                  "Target Job Position"}
              </p>


              <div className="resume-preview-contact">

                {resume.email && (
                  <span>
                    {resume.email}
                  </span>
                )}

                {resume.phone && (
                  <span>
                    {resume.phone}
                  </span>
                )}

                {resume.location && (
                  <span>
                    {resume.location}
                  </span>
                )}

              </div>


              {resume.linkedin && (

                <div className="resume-preview-link">
                  {resume.linkedin}
                </div>

              )}

            </div>


            {/* SUMMARY */}

            {generatedResume?.professional_summary && (

              <div className="resume-preview-section">

                <h3>
                  Professional Summary
                </h3>

                <p>
                  {generatedResume.professional_summary}
                </p>

              </div>

            )}

{/* SKILLS */}

{generatedResume?.skills?.length > 0 && (

  <div className="resume-preview-section">

    <h3>
      Skills
    </h3>

    <ul className="resume-preview-skills-list">

      {generatedResume.skills.map(
        (skill, index) => (

          <li
            key={index}
            className="resume-preview-skill-item"
          >
            {skill}
          </li>

        )
      )}

    </ul>

  </div>

)}



            {/* EXPERIENCE */}

            {generatedResume?.work_experience?.length > 0 && (

              <div className="resume-preview-section">

                <h3>
                  Work Experience
                </h3>


                {generatedResume.work_experience.map(
                  (experience, index) => (

                    <div
  key={index}
  className="resume-preview-experience-item"
>
                      

                      {experience.title && (
                        <h4>
                          {experience.title}
                        </h4>
                      )}


                      {(experience.company ||
                        experience.dates) && (

                        <p>

                          {experience.company}

                          {experience.company &&
                            experience.dates &&
                            " | "}

                          {experience.dates}

                        </p>

                      )}


                      {experience.responsibilities?.length > 0 && (

                        <ul>

                          {experience.responsibilities.map(
                            (item, itemIndex) => (

                              <li key={itemIndex}>
                                {item}
                              </li>

                            )
                          )}

                        </ul>

                      )}

                    </div>

                  )
                )}

              </div>

            )}

{generatedResume?.education?.length > 0 && (
  <div className="resume-preview-section">
    <h3>Education</h3>

    {generatedResume.education.map(
      (education, index) => (
        <div
          key={index}
          className="resume-preview-education-item"
        >
          {education.degree && (
            <h4>{education.degree}</h4>
          )}

          {education.specialization && (
            <p>
              {education.specialization}
            </p>
          )}

          {(education.institution ||
            education.year) && (
            <p>
              {education.institution}

              {education.institution &&
                education.year &&
                " | "}

              {education.year}
            </p>
          )}
        </div>
      )
    )}
  </div>
)}

            {/* PROJECTS */}

            {generatedResume?.projects?.length > 0 && (

              <div className="resume-preview-section">

                <h3>
                  Projects
                </h3>


                <ul>

                  {generatedResume.projects.map(
                    (project, index) => (

                   <li key={index} className="resume-preview-project-item">

  {typeof project === "string" ? (

    <span className="resume-preview-project-description">
      {project}
    </span>

  ) : (

    <>

      {(project.name || project.title) && (
        <span className="resume-preview-project-name">
          {project.name || project.title}
        </span>
      )}

  {project.technologies?.length > 0 && (
  <div className="resume-preview-project-tech">
    {project.technologies.map((technology, techIndex) => (
      <span key={techIndex}>
        {technology}
      </span>
    ))}
  </div>
)}

      {project.description && (
        <span className="resume-preview-project-description">
          {project.description}
        </span>
      )}

    </>

  )}

</li>

                    )
                  )}

                </ul>

              </div>

            )}


            {/* CERTIFICATIONS */}

            {generatedResume?.certifications?.length > 0 && (

              <div className="resume-preview-section">

                <h3>
                  Certifications
                </h3>


                <ul>

                  {generatedResume.certifications.map(
                    (certification, index) => (

                      <li key={index}>

                        {typeof certification === "string"
                          ? certification
                          : (
                            <>
                              {certification.name || ""}

                              {certification.organization &&
                                ` — ${certification.organization}`}

                              {certification.date &&
                                ` (${certification.date})`}
                            </>
                          )}

                      </li>

                    )
                  )}

                </ul>

              </div>

            )}


           {/* LANGUAGES */}

{generatedResume?.languages?.length > 0 && (

  <div className="resume-preview-section">

    <h3>
      Languages
    </h3>

    <div className="resume-preview-languages">

      {generatedResume.languages.map(
        (language, index) => (

          <span
            key={index}
            className="resume-preview-language"
          >
            {language}
          </span>

        )
      )}

    </div>

  </div>

)}

          </div>

        </section>

      </div>

    </div>
  );
}


export default ResumeBuilder;