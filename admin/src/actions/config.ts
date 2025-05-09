"use server";

import { api } from "../api/api";

export async function configList(){
  return await api.configList({});
}