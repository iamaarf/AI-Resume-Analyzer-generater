import { useEffect, useState } from "react";
import "./AdminDashboard.css";
import AdminLogout from "./AdminLogout.jsx";

const API_BASE_URL =
  "https://ai-resume-analyzer-generater.onrender.com";

const getAdminHeaders = () => {
  const token =
    localStorage.getItem(
      "admin_access_token"
    );

  return {
    Authorization: `Bearer ${token}`,
  };
};

function AdminDashboard() {
  const [analytics, setAnalytics] = useState(null);
  const [dailyAnalytics, setDailyAnalytics] = useState([]);
  const [monthlyAnalytics, setMonthlyAnalytics] = useState([]);
  const [yearlyAnalytics, setYearlyAnalytics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([
      fetch(
        `${API_BASE_URL}/admin/analytics`,
        {
          headers: getAdminHeaders(),
        }
      ),

      fetch(
        `${API_BASE_URL}/admin/analytics/daily`,
        {
          headers: getAdminHeaders(),
        }
      ),

      fetch(
        `${API_BASE_URL}/admin/analytics/monthly`,
        {
          headers: getAdminHeaders(),
        }
      ),

      fetch(
        `${API_BASE_URL}/admin/analytics/yearly`,
        {
          headers: getAdminHeaders(),
        }
      )
    ])
      .then(
        async ([
          analyticsResponse,
          dailyResponse,
          monthlyResponse,
          yearlyResponse
        ]) => {
          if (
            !analyticsResponse.ok ||
            !dailyResponse.ok ||
            !monthlyResponse.ok ||
            !yearlyResponse.ok
          ) {
            throw new Error(
              "Failed to load analytics."
            );
          }

          const analyticsData =
            await analyticsResponse.json();

          const dailyData =
            await dailyResponse.json();

          const monthlyData =
            await monthlyResponse.json();

          const yearlyData =
            await yearlyResponse.json();

          return {
            analyticsData,
            dailyData,
            monthlyData,
            yearlyData
          };
        }
      )
      .then(
        ({
          analyticsData,
          dailyData,
          monthlyData,
          yearlyData
        }) => {
          setAnalytics(analyticsData);
          setDailyAnalytics(dailyData);
          setMonthlyAnalytics(monthlyData);
          setYearlyAnalytics(yearlyData);
        }
      )
      .catch((error) => {
        console.error(error);

        setError(
          error.message ||
            "Unable to load analytics."
        );
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="admin-dashboard">
        <div className="admin-dashboard-header">
          <h1>Admin Analytics</h1>
          <p>Loading analytics...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="admin-dashboard">
        <div className="admin-dashboard-header">
          <h1>Admin Analytics</h1>

          <p>
            {error}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="admin-dashboard">

      {/* HEADER */}

      <div className="admin-dashboard-header">
        <div className="admin-dashboard-title-row">

          <div>

            <div className="admin-dashboard-badge">
              <span className="admin-dashboard-badge-dot"></span>
              LIVE ANALYTICS
            </div>

            <h1>
              Admin Analytics
            </h1>

            <p>
              Resume Analyzer usage and
              performance overview.
            </p>

          </div>
<div className="admin-dashboard-header-actions">
  <div className="admin-dashboard-status">
    <span>●</span>
    System Active
  </div>

  <AdminLogout />
</div>

        </div>
      </div>


      {/* KPI CARDS */}

      {analytics && (
        <div className="analytics-grid">

          <div className="analytics-card analytics-card-primary">

            <div className="analytics-card-top">
              <span>📄</span>
              <small>ANALYSES</small>
            </div>

            <h3>
              Total Resume Analyses
            </h3>

            <strong>
              {analytics.total_analyses}
            </strong>

            <p>
              All completed resume analyses
            </p>

          </div>


          <div className="analytics-card">

            <span>🎯</span>

            <h3>
              Average ATS Score
            </h3>

            <strong>
              {analytics.average_ats_score}/100
            </strong>

          </div>


          <div className="analytics-card">

            <span>💼</span>

            <h3>
              Job Description Used
            </h3>

            <strong>
              {analytics.job_description_used}
            </strong>

          </div>


          <div className="analytics-card">

            <span>📝</span>

            <h3>
              Job Description Not Used
            </h3>

            <strong>
              {analytics.job_description_not_used}
            </strong>

          </div>

        </div>
      )}


      {/* 7-DAY ACTIVITY */}

      <div className="daily-analytics-section">

        <div className="daily-analytics-header">

          <div>

            <h2>
              7-Day Activity
            </h2>

            <p>
              Resume analyses completed
              over the last 7 days.
            </p>

          </div>

        </div>


        <div className="daily-analytics-list">

          {dailyAnalytics.map((day) => (

            <div
              className="daily-analytics-row"
              key={day.date}
            >

              <div className="daily-analytics-date">
                {day.date}
              </div>


              <div className="daily-analytics-bar-wrapper">

                <div
                  className="daily-analytics-bar"
                  style={{
                    width: `${Math.min(
                      day.analyses * 20,
                      100
                    )}%`
                  }}
                ></div>

              </div>


              <strong className="daily-analytics-count">
                {day.analyses}
              </strong>

            </div>

          ))}

        </div>

      </div>


      {/* MONTHLY ACTIVITY */}

      <div className="monthly-analytics-section">

        <div className="monthly-analytics-header">

          <div>

            <h2>
              Monthly Activity
            </h2>

            <p>
              Resume analyses completed
              month by month.
            </p>

          </div>

        </div>


        <div className="monthly-analytics-list">

          {monthlyAnalytics.map((month) => (

            <div
              className="monthly-analytics-row"
              key={month.month}
            >

              <div className="monthly-analytics-date">
                {month.month}
              </div>


              <div className="monthly-analytics-bar-wrapper">

                <div
                  className="monthly-analytics-bar"
                  style={{
                    width: `${Math.min(
                      month.analyses * 10,
                      100
                    )}%`
                  }}
                ></div>

              </div>


              <strong className="monthly-analytics-count">
                {month.analyses}
              </strong>

            </div>

          ))}

        </div>

      </div>


      {/* YEARLY ACTIVITY */}

      <div className="yearly-analytics-section">

        <div className="yearly-analytics-header">

          <div>

            <h2>
              Yearly Activity
            </h2>

            <p>
              Resume analyses completed
              year by year.
            </p>

          </div>

        </div>


        <div className="yearly-analytics-list">

          {yearlyAnalytics.map((year) => (

            <div
              className="yearly-analytics-row"
              key={year.year}
            >

              <div className="yearly-analytics-date">
                {year.year}
              </div>


              <div className="yearly-analytics-bar-wrapper">

                <div
                  className="yearly-analytics-bar"
                  style={{
                    width: `${Math.min(
                      year.analyses * 10,
                      100
                    )}%`
                  }}
                ></div>

              </div>


              <strong className="yearly-analytics-count">
                {year.analyses}
              </strong>

            </div>

          ))}

        </div>

      </div>

    </div>
  );
}

export default AdminDashboard;