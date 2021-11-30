using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public static class JsonHelper
{
    public static T[] FromJson<T>(string json)
    {
        Wrapper<T> wrapper = JsonUtility.FromJson<Wrapper<T>>(json);
        return wrapper.Items;
    }

    public static string ToJson<T>(T[] array)
    {
        Wrapper<T> wrapper = new Wrapper<T>();
        wrapper.Items = array;
        return JsonUtility.ToJson(wrapper);
    }

    public static string ToJson<T>(T[] array, bool prettyPrint)
    {
        Wrapper<T> wrapper = new Wrapper<T>();
        wrapper.Items = array;
        return JsonUtility.ToJson(wrapper, prettyPrint);
    }

    [System.Serializable]
    private class Wrapper<T>
    {
        public T[] Items;
    }
}

[System.Serializable]
class MyCar
{
    public int x;
    public int y;

    override public string ToString()
    {
        return "X: " + x + ", Y: " + y;
    }
}

public class MoverAuto : MonoBehaviour
{
    string simulationURL = null;
    private float waitTime = 0.3f;
    private float timer = 0.0f;
    public GameObject[] myCars;

    // Start is called before the first frame update
    void Start()
    {
        StartCoroutine(ConnectToMesa());
    }

    IEnumerator ConnectToMesa()
    {
        WWWForm form = new WWWForm();

        using (UnityWebRequest www = UnityWebRequest.Post("https://movilidad-urbana-trafico-chipper-kookaburra-gj.eu-gb.mybluemix.net/games", form))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.Log(www.error);
            }
            else
            {
                simulationURL = www.GetResponseHeader("Location");
                Debug.Log("Connected to simulation through Web API");
                Debug.Log(simulationURL);
            }
        }
    }

    IEnumerator UpdatePositions()
    {
        using (UnityWebRequest www = UnityWebRequest.Get(simulationURL))
        {
            if (simulationURL != null)
            {
                // Request and wait for the desired page.
                yield return www.SendWebRequest();

                //Debug.Log(www.downloadHandler.text);
                Debug.Log("Data has been processed");
                MyCar[] cars = JsonHelper.FromJson<MyCar>(www.downloadHandler.text);
                //Debug.Log(cars[0].ToString());
                //Debug.Log(cars[1].ToString());
                float zVal = 0f;
                myCars[0].transform.LookAt(new Vector3(cars[0].x,  0, cars[0].y), transform.up);
                myCars[0].transform.position = new Vector3(cars[0].x, 0, cars[0].y);

                myCars[1].transform.LookAt(new Vector3(cars[1].x, 0, cars[1].y), transform.up);
                myCars[1].transform.position = new Vector3(cars[1].x, 0, cars[1].y);

                myCars[2].transform.LookAt(new Vector3(cars[2].x, 0, cars[2].y), transform.up);
                myCars[2].transform.position = new Vector3(cars[2].x, 0, cars[2].y);

                myCars[3].transform.LookAt(new Vector3(cars[3].x, 0, cars[3].y), transform.up);
                myCars[3].transform.position = new Vector3(cars[3].x, 0, cars[3].y);

                myCars[4].transform.LookAt(new Vector3(cars[4].x, 0, cars[4].y), transform.up);
                myCars[4].transform.position = new Vector3(cars[4].x, 0, cars[4].y);
            }
        }
    }

    // Update is called once per frame
    void Update()
    {
        timer += Time.deltaTime;
        if (timer > waitTime)
        {
            StartCoroutine(UpdatePositions());
            timer = timer - waitTime;
        }
    }
}
